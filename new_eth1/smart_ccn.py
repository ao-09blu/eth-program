import json
from web3 import Web3
from solcx import compile_source, install_solc
import web3
import subprocess
import re
import cefpyco
import time

def get_private_key(account_addr_C, Pass):#checksumをしておく
    proc = subprocess.run('node get_key.js '+ account_addr_C + " " +  Pass, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#jsonファイルとパスワードからkeyを取得
    print(proc.stdout)
    print(proc.stderr)
    key_array = re.findall("\d+",proc.stdout.decode('cp932'))#keyの中身を配列に格納
    privatekey = ""
    for i in range(len(key_array)):
        key_array[i] = format(int(key_array[i]), 'x')
        privatekey += key_array[i]
    return privatekey

def make_private_key(P_key):
    key_array = re.findall("\d+",P_key)#keyの中身を配列に格納
    privatekey = ""
    for i in range(len(key_array)):
        key_array[i] = format(int(key_array[i]), 'x')
        privatekey += key_array[i]
    return privatekey

def read_ip_add():#自身のIPアドレスを取得
    proc = subprocess.run("ip a", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#ip aコマンド結果取得
    address_array = re.findall("192\.168\.72\.\d+", proc.stdout.decode("cp932"))#ipアドレス取得
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
http_port = 8101
my_ip_addr = read_ip_add() #get IP addr.

helloPrefix = "ccnx:/" + "hello"
func_array = ["/connect", "/ABI", "/C_addr", "/hop_list"]
#FIBから接続しているノードのFace番号とIPaddrを取得
facenum = facenum_FIB(helloPrefix)
faceaddr = []
print(facenum)

for i in range(len(facenum)):
    print(facenum[i])
    faceaddr.append(faceid_FIB(facenum[i]))
    print("facenum:" + facenum[i] + "faceaddress: " + faceaddr[i])




#ethereumの起動
#start_up = "geth --networkid " + str(networkid) + " --allow-insecure-unlock --maxpeers " + str(maxpeers) + " --nodiscover --datadir " + datadir +  "--http --http.addr "+ my_ip_addr + " --http.port "+ str(http_port) +" console 2>> " + datadir + "/geth.log"
#proc = subprocess.run(start_up, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)



Pass_word = "aaaaaaaaaa"#自分のパスワード
my_Account_num = 0 #アカウントの番号

#イーサリアムに接続
#w3 = Web3(web3.HTTPProvider("http://localhost:"+str(http_port)))
w3 = Web3(web3.HTTPProvider("http://"+my_ip_addr+":8101"))


#自身のenode情報を格納
node_info = w3.geth.admin.node_info()#enode情報を格納
print(node_info)
print(node_info.enode)
enode_addr = re.sub("@.+", "", node_info.enode)#@以降を削除

enode_addr = enode_addr +"@" + my_ip_addr + ":30303"#相手が登録できる形に変更“enode:// <enode addr.> @ <自身のIP addr.>”


print("enode_addr: " + enode_addr)

#自身のアドレス設定と鍵の入手
myAddr = w3.toChecksumAddress(w3.eth.accounts[1])
#privatekey = get_private_key(myAddr, Pass_word)
P_key="33 16 226 84 72 62 245 87 75 45 59 236 222 156 181 194 202 105 197 208 123 102 49 195 176 153 31 250 69 47 83 104"
privatekey = make_private_key(P_key)
print("privatekey")
print(privatekey)



# マイニング設定(起動時に設定しないとだめ?) or マイナーの設定は手動でやる??
# Solidity のソースをコンパイル 文章を生成するようにすればいけそう?
install_solc("0.5.16")
compiled_sol = compile_source(
    '''
    pragma solidity >=0.5.16;

    //配列を返す&入力できるように
    pragma experimental ABIEncoderV2;

    contract Greeter {
        //必要な情報の宣言

        //コンテンツ情報の登録
        struct Contents_info{
            string name; //コンテンツ名
            address producer; //コンテンツの配信者のアドレス
            uint router_ID;
            string[] keyword;
        }
        //コンテンツ配信者の登録
        struct Producer{
            string Pname;
            address ip_add;
        }
        struct Router{
            uint RouterID;
            string[] neighbor; 
        }

        Contents_info[] public contents_list;//contents_infoの配列宣言
        mapping(address=>Router) public Link_DB;
        uint ID = 0;
        //関数

        //コンテンツの登録
        function regist_content(string memory _name, uint _routerID, string[] memory _keyword) public returns(uint){
            uint id = contents_list.push(Contents_info({
                name: _name,
                producer: msg.sender,
                router_ID: _routerID,
                keyword: _keyword
            }));
            return (id-1);
        }

        function regist_router(string[] memory _neighbor)public{
            Link_DB[msg.sender].RouterID = ID;
            Link_DB[msg.sender].neighbor = _neighbor;
            ID = ID + 1;
        }

        function update_router(string[] memory _neighbor) public{
            Link_DB[msg.sender].neighbor = _neighbor;
        }

        function show_router() view public returns (uint){
            return Link_DB[msg.sender].RouterID;
        }

        function show_contents() view public returns (Contents_info[] memory) {
            uint list_length = contents_list.length;
            Contents_info[] memory content_array = new Contents_info[](list_length);
            content_array = contents_list;
            return content_array;
        }
    }
    ''',
    output_values=['abi', 'bin']
)

# コントラクトインターフェイス
contract_id, contract_interface = compiled_sol.popitem()

# バイトコードとABI
bytecode = contract_interface['bin']
abi = contract_interface['abi']

#ABIの表示
print("ABI")
print(abi)

# コントラクトの作成
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

#トランザクションの生成
tx = contract.constructor().buildTransaction({
    'from': myAddr,
    'nonce': w3.eth.getTransactionCount(myAddr),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')})


signed_tx = w3.eth.account.signTransaction(tx, privatekey) #privatekeyで署名
#signed_tx = w3.eth.account.signTransaction(tx)#署名はclefがやってくれる??
tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction) #トランザクションの送信

print(w3.toHex(tx_hash)) #トランザクションIDの取得

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash) #生成されたコントラクトアドレスの取得(マイニングしてないと進まない)
print("Contract Deployed At:", tx_receipt['contractAddress'])

Networking_contract_id = tx_receipt['contractAddress']

print(Networking_contract_id)

start_time = time.time()

NCI_C = w3.toChecksumAddress(Networking_contract_id)
contract_instance = w3.eth.contract(abi=abi, address=NCI_C)

#初期登録情報の登録
neighbor = []#自分の近隣情報(string型にしないとまずいかも?)
tx = contract_instance.functions.regist_router(neighbor).buildTransaction({
    'from': myAddr,
    'nonce': w3.eth.getTransactionCount(myAddr),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, privatekey)
#トランザクションの送信
tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

my_router_id = contract_instance.functions.show_router().call()
print(my_router_id)
my_interest_prefix = "ccnx:/node" +str(my_router_id)


#content1の登録
key = ["hello", "test", "key"]
tx = contract_instance.functions.regist_content("content1", my_router_id ,key).buildTransaction({
    'from': myAddr,
    'nonce': w3.eth.getTransactionCount(myAddr),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, privatekey)
#トランザクションの送信
tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#content2の登録
key = ["introduction", "connect", "words"]
tx = contract_instance.functions.regist_content("content2", my_router_id, key).buildTransaction({
    'from': myAddr,
    'nonce': w3.eth.getTransactionCount(myAddr),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})
signed_tx = w3.eth.account.signTransaction(tx, privatekey)
#トランザクションの送信
tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
hop_count = [0] * 100 #hop数を管理するカウント

print("Contract value: {}".format(contract_instance.functions.show_contents().call()))






with cefpyco.create_handle() as handle:
    #handle.send_interest()#最初のノードはやらない
    handle.register(helloPrefix)#helloを受信する用
    handle.register(my_interest_prefix)

    #接続ループをつくるべき? 接続でfunc_array = ["connect", "ABI", "C_addr"]きたら削除??
    while True:
        info = handle.receive()#packetの受信
        if info.is_succeeded:#packetが受信成功
            if info.is_interest:#interestパケットの場合
                if helloPrefix in info.name: #hello interestだった場合
                    if func_array[0] in info.name:#connect Interest
                        print("Receive hello Interst: {}" .format(info))
                        handle.send_data(info.name, enode_addr, info.chunk_num, expiry=3600000, cache_time=36000000)#自分のenodeアドレスをDataとして返送
                        print("send Data to reply hello_Interest")
                    elif func_array[1] in info.name:#ABIを取得するためのInterest
                        print("Receive Networking ABI Interest: {}" .format(info))
                        handle.send_data(info.name, abi, info.chunk_num, expiry=3600000, cache_time=36000000)#コントラクトのABIを送信
                    elif func_array[2] in info.name:
                        print("Receive Networking contract ID Interest: {}" .format(info))
                        handle.send_data(info.name, Networking_contract_id, info.chunk_num ,expiry=3600000, cache_time=360000000)
                    elif func_array[3] in info.name:
                        print("Receive hop_list Interest: {}" .format(info))
                        handle.send_data(info.name, hop_count, info.chunk_num, expiry=3600000, cache_time=36000000)
                    
                elif my_interest_prefix in info.name:
                    print("Receive interest: {}".format(info))
                    handle.send_data(info.name, "data", info.chunk_num, expiry=3600000, cache_time=36000000)
  
            if info.is_data:#dataパケットの場合
                if helloPrefix in info.name:#接続要求パケットに対するDataの場合
                    if func_array[0] in info.name:
                        w3.geth.admin.add_peer(info.payload_s)#取得したデータが相手のenodeアドレスであるため、利用して登録
                        print("Regist peer")
                        #abiとcontractIDを要求する
                        handle.deregister(helloPrefix)
                        handle.send_interest(helloPrefix+func_array[1], 0)#abiに対する要求
                        handle.send_interest(helloPrefix+func_array[2], 0)#contract_idに対する要求
                        handle.register(helloPrefix)
                    elif func_array[1] in info.name:
                        abi = info.payload
                        print("get abi")
                        print(abi)
                    elif func_array[2] in info.name:
                        Networking_contract_id = info.payload
                        print("get contract ID")
                        print(Networking_contract_id)
                    
                    elif func_array[3] in info.name:
                        print(info.payload)
                        #payloadを分割する必要あり??配列になっている??
                        print(info.payload[0])
                            



        end_time = time.time()
        elapsed_time = end_time - start_time
        contract_instance = w3.eth.contract(abi=abi, address=Networking_contract_id)
        if(elapsed_time > 20):#20秒立ったら
            print("Contract value: {}".format(contract_instance.functions.show_contents().call()))#コンテンツリストの確認
            start_time = end_time #現在時間から計測


                






#