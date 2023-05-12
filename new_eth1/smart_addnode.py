import json
from web3 import Web3
from solcx import compile_source, install_solc
import web3
import subprocess
import re
import cefpyco

def get_private_key(account_addr_C, Pass):#checksumをしておく
    proc = subprocess.run('node get_key.js '+ account_addr_C + " " +  Pass, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#jsonファイルとパスワードからkeyを取得
    key_array = re.findall("\d+",proc.stdout.decode('cp932'))#keyの中身を配列に格納
    privatekey = ""
    for i in range(len(key_array)):
        key_array[i] = format(int(key_array[i]), 'x')
        privatekey += key_array[i]
    return privatekey

def read_ip_add():#自身のIPアドレスを取得
    proc = subprocess.run("ip a", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#ip aコマンド結果取得
    address_array = re.findall("192\.168\.72\.\d+", proc.stdout.decode("cp932"))#ipアドレス取得
    print(address_array)
    return address_array[0]#おそらく必要なところ返せる

#CCN
#最初にFIBに接続しているノードの情報を取ってくる
def facenum_FIB(contentsname):#FIBの中からFace番号を読み取る
    searchnum='cefstatus | grep -A 1 \"' + contentsname + '\" | grep \"Faces\"'
    proc = subprocess.run(searchnum, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    facenum=re.findall(".*?(\d+).*?", proc.stdout.decode('cp932'))
    return facenum#Face番号の配列を返す

def faceid_FIB(facenum):#FIBの中からfacenumに対応したaddressを返す
    searchaddress='cefstatus | grep \"faceid\" | grep \" ' + facenum + ' \"'
    proc = subprocess.run(searchaddress, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    faceadd=re.findall(".*?(\d+.\d+.\d+.\d+):.*?", proc.stdout.decode('cp932'))
    print("faceadd:" + str(faceadd))
    return faceadd[0]#対応したaddressを返す

def end_check(mysequence, updatenum, shareContentnum):
    flag=1
    for i in range(shareContentnum):
        if mysequence[i]!=updatenum:
            flag=0
    return flag
    

def facenum_tosendI(preinterestname):#送信されてきたpreInterestがどのFace番号化を読み取る
    searchnum ='cefstatus | grep -A 1 \"' + preinterestname + "\" | grep \"Faces\""
    proc = subprocess.run(searchnum, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    facenum=re.findall(".*?(\d+).*?",proc.stdout.decode('cp932'))
    return facenum[0]#文字列形式で返す


def FIBregist(preI, Interestpre, facenum, faceadd):#preInterestnameからFace番号を読み取り、そのFace番号にコンテンツがあると仮定してFIBに追加する
    nowface=facenum_tosendI(preI)
    for i in range(len(facenum)):
        if nowface==facenum[i]:#preInterest送信元に対するInterestのFIBを追加
            addroute='sudo cefroute add ' + Interestpre + ' udp ' + faceadd[i]
            proc = subprocess.run(addroute, shell=True)
            #print("Add route " + Interestpre + " Face: " + facenum[i])
        else:#Interest送信元以外に対するpre Interest転送用のFace番号の追加
            addroute= 'sudo cefroute add ' + preI + ' udp ' + faceadd[i]
            proc = subprocess.run(addroute, shell=True)
            #print("Add route " + preI + " Face: " + facenum[i])

def FIBderegist(FIBname, faceadd):
    for i in range(len(faceadd)):
        delroute='sudo cefroute del ' + FIBname + ' udp ' + faceadd[i]
        proc = subprocess.run(delroute, shell=True)
        #print("Del route " + FIBname + " Face:" + facenum[i])

def FIBregistall(FIBname, faceadd):
    for i in range(len(faceadd)):
        addroute= 'sudo cefroute add ' + FIBname + ' udp ' + faceadd[i]
        proc = subprocess.run(addroute, shell=True)
        #print("Add route " + preI + " Face: " + facenum[i])



def interest_history(interestname):#そのinterestが既にFIBに登録されているかどうかを判別
    search = 'cefstatus | grep -A 1 \"' + interestname + "\" | grep \"Faces\""
    proc = subprocess.run(search, shell=True,  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (proc.stdout.decode('cp932')==""):#既にFIBに登録済みであった場合
        flag=1
    else:#登録を行っていなかった場合
        flag=0
    return flag#interestを送信済みの場合は1を、まだinterestを返していない場合は0を返す

networkid = 100
maxpeers = 10
datadir = "/new_eth2"
http_port = 8101
my_ip_addr = read_ip_add() #get IP addr.

helloPrefix = "ccnx:/" + "hello"
func_array = ["/connect", "/ABI", "/C_addr"]
#FIBから接続しているノードのFace番号とIPaddrを取得
facenum = facenum_FIB(helloPrefix)
faceaddr = []
print(facenum)

for i in range(len(facenum)):
    print(facenum[i])
    faceaddr.append(faceid_FIB(facenum[i]))
    print("facenum:" + facenum[i] + "faceaddress: " + faceaddr[i])







Pass_word = "ethenode0002"#自分のパスワード
my_Account_num = 0 #アカウントの番号

#イーサリアムに接続
w3 = Web3(web3.HTTPProvider("http://" + my_ip_addr + ":" + str(http_port)))



#自身のenode情報を格納
node_info = w3.geth.admin.node_info()#enode情報を格納
print(node_info)
print(node_info.enode)
enode_addr = re.sub("@.+", "", node_info.enode)#@以降を削除

enode_addr = enode_addr +"@" + my_ip_addr + ":30303"#相手が登録できる形に変更“enode:// <enode addr.> @ <自身のIP addr.>”
print("enode_addr: " + enode_addr)


with cefpyco.create_handle() as handle:
    #handle.send_interest()#最初のノードはやらない
    connectI_name = helloPrefix + func_array[0]
    handle.send_interest(connectI_name, 0)
    handle.register(helloPrefix)#helloを受信する用
    
    while True:
        info = handle.receive()#packetの受信
        if info.is_succeeded:#packetが受信成功
            if info.is_interest:#interestパケットの場合
                if helloPrefix in info.name: #hello interestだった場合
                    if func_array[0] in info.name:#connect Interest
                        print("Receive hello Interst: {}" .format(info))
                        handle.send_data(info.name, enode_addr, info.chunk_num, expiry=3600000, cache_time=0)#自分のenodeアドレスをDataとして返送
                        print("send Data to reply hello_Interest")
                    elif func_array[1] in info.name:#ABIを取得するためのInterest
                        print("Receive Networking ABI Interest: {}" .format(info))
                        handle.send_data(info.name, abi, info.chunk_num, expiry=3600000, cache_time=0)#コントラクトのABIを送信
                    elif func_array[2] in info.name:
                        print("Receive Networking contract ID Interest: {}" .format(info))
                        handle.send_data(info.name, Networking_contract_id, expiry=3600000, cache_time=0)
  
            if info.is_data:#dataパケットの場合
                if helloPrefix in info.name:#接続要求パケットに対するDataの場合
                    if func_array[0] in info.name:#connectパケットの場合
                        w3.geth.admin.add_peer(info.payload_s)#取得したデータが相手のenodeアドレスであるため、利用して登録
                        print("Regist peer")
                        #abiとcontractIDを要求する
                        handle.deregister(helloPrefix)
                        handle.send_interest(helloPrefix+func_array[1], 0)#abiに対する要求
                        print("send ABI Interest")
                        handle.send_interest(helloPrefix+func_array[2], 0)#contract_idに対する要求
                        print("send contract address Interest")
                        handle.register(helloPrefix)
                    elif func_array[1] in info.name:
                        abi = info.payload
                        print("get abi")
                        print(abi)
                    elif func_array[2] in info.name:
                        Networking_contract_id = info.payload
                        print("get contract ID")
                        print(Networking_contract_id)