import json
from web3 import Web3
from solcx import compile_source, install_solc
import web3
import subprocess
import re
import cefpyco
import time
import sys
import ast


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
        privatekey += key_array[i].zfill(2)
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

def dijkstra(graph, start):
    #初期化
    n = len(graph)
    visited = [False] * n
    distance = [sys.maxsize] * n
    distance[start] = 0
    #u=start
    previous = [None] * n
    #ダイクストラ法
    for i in range(n):
        #未処理の中で最小の距離を持つ頂点を探す
        min_distance = sys.maxsize
        print(distance)
        print(visited)
        print(min_distance)

        for j in range(n):
            if not visited[j] and distance[j] < min_distance: #未到達かつ最小の距離を見つける
                min_distance = distance[j]
                u = j
                
        #訪問済みにする
        visited[u] = True

        #uから到達可能な頂点の距離を更新する
        for v in range(n):
            if not visited[v] and graph[u][v] != 0:
                new_distance = distance[u] + graph[u][v]
                if new_distance < distance[v]:
                    distance[v] = new_distance
                    previous[v] = u
            
    # 最短経路の頂点リストを作成する
    path = []
    for i in range(n):
        path.append([])
        if i == start:
            continue
        if previous[i] is not None:
            node = i
            while node is not None:
                path[i].insert(0, node)
                node = previous[node]
        else:
            path.append(None)
    # 最短経路上の頂点リストを返す
    #return path
    nextid = []
    for i in range(n):
        if(i==start):#startノードの場合
            nextid = -1
        else:#それ以外の場合
            nextid.push(path[i][1])#スタートノードの次を格納
    
    return nextid
        
def make_FIB(neigbor_array, myrouterID,content_array, IP_addr, registed_num):
    #dijkstra法
    n = len(neigbor_array)
    visited = [False] * n
    distance = [sys.maxsize] * n
    distance[myrouterID] = 0
    #u=start
    previous = [None] * n
    #ダイクストラ法
    for i in range(n):
        #未処理の中で最小の距離を持つ頂点を探す
        min_distance = sys.maxsize
        print(distance)
        print(visited)
        print(min_distance)

        for j in range(n):
            if not visited[j] and distance[j] < min_distance: #未到達かつ最小の距離を見つける
                min_distance = distance[j]
                u = j
                
        #訪問済みにする
        visited[u] = True

        #uから到達可能な頂点の距離を更新する
        for v in range(n):
            if not visited[v] and neigbor_array[u][v] != 0:
                new_distance = distance[u] + neigbor_array[u][v]
                if new_distance < distance[v]:
                    distance[v] = new_distance
                    previous[v] = u
            
    # 最短経路の頂点リストを作成する
    path = []
    for i in range(n):
        path.append([])
        if i == myrouterID:
            continue
        if previous[i] is not None:
            node = i
            while node is not None:
                path[i].insert(0, node)
                node = previous[node]
        else:
            path.append(None)
    # 最短経路上の頂点リストを返す
    #return path
    nextid = []
    for i in range(n):
        if(i==myrouterID):#startノードの場合
            nextid.append(-1)
        else:#それ以外の場合
            nextid.append(path[i][1])#スタートノードの次を格納


    for i in range(len(content_array)-registed_num):#登録していないコンテンツに対してループ
        Prefix = "ccnx:/" + content_array[i+registed_num][0]#コンテンツ名を取得
        print(Prefix)
        nearest_ID = find_nearest(distance, content_array[i+registed_num][2], myrouterID=myrouterID)
        print("New Content:" + content_array[i+registed_num][0] + " Nearest content holder is Node" + str(nearest_ID))
        print(myrouterID)
        if(nearest_ID!=myrouterID):#一番近いノードが自分でない場合
            addroute='sudo cefroute add ' + Prefix + ' udp ' + IP_addr[nextid[nearest_ID]]
            proc = subprocess.run(addroute, shell=True)
            print("Add route " + Prefix + " Next Face:" + str(nextid[nearest_ID]))

        
def find_nearest(distance_list, content_holder,myrouterID):
    min_distance = sys.maxsize
    nearest_id = myrouterID
    print(distance_list)
    for i in range(len(content_holder)):#コンテンツ所持者の数だけループ
        if distance_list[content_holder[i]]!=0 and distance_list[content_holder[i]] < min_distance:#自分以外かつ距離が小さいものの場合
            print("find min")
            min_distance = distance_list[content_holder[i]]
            nearest_id = content_holder[i] 
   
    return nearest_id

def make_neighbor(connection_target, registed_router_num):
    neighbor_list = []#登録するルータは0それ以外は1を登録
    for i in range(registed_router_num):
        if(i in connection_target):
            neighbor_list.append(1)
        else:
            neighbor_list.append(0)
    return neighbor_list






networkid = 101
maxpeers = 10
http_port = 8101
my_ip_addr = read_ip_add() #get IP addr.

helloPrefix = "ccnx:/" + "hello"
func_array = ["/connect", "/ABI", "/C_addr"]
my_content_array = [] #自分の持っているコンテンツを登録
Req_flag = [0,0,0]
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



Pass_word = "ethenode0001"#自分のパスワード
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
myAddr = w3.toChecksumAddress(w3.eth.accounts[0])
#privatekey = get_private_key(myAddr, Pass_word)
P_key="12 189 28 87 76 155 162 0 23 17 110 242 125 41 180 39 43 248 222 66 105 72 252 90 82 212 238 237 86 234 11 153"
privatekey = make_private_key(P_key)
print("privatekey")
print(privatekey)

connection_target = [0]

start_time = time.time()

with cefpyco.create_handle() as handle:
    #handle.send_interest()#最初のノードはやらない
    connect_prefix = helloPrefix + func_array[0]
    print("send hello Interest")
    print(connect_prefix)
    handle.send_interest(connect_prefix, 0)#connect_interestの送信
    handle.register(helloPrefix)#helloを受信する用

    #接続用ループ
    while True:
        info = handle.receive()
        if info.is_data:#dataパケットの場合
                if helloPrefix in info.name:#接続要求パケットに対するDataの場合
                    if func_array[0] in info.name:
                        w3.geth.admin.add_peer(info.payload_s)#取得したデータが相手のenodeアドレスであるため、利用して登録
                        print("Regist peer")
                        #abiとcontractIDを要求する
                        handle.deregister(helloPrefix)
                        handle.send_interest(helloPrefix+func_array[1], 0)#abiに対する要求
                        handle.send_interest(helloPrefix+func_array[2], 0)#contract_idに対する要求
                        Req_flag[0] = 1
                        handle.register(helloPrefix)
                    elif func_array[1] in info.name:
                        abi = info.payload_s
                        print("get abi")
                        print(abi)
                        Req_flag[1] = 1
                        #修正
                        abi = ast.literal_eval(abi)
                        print(type(abi))
                    elif func_array[2] in info.name:
                        Networking_contract_id = info.payload_s
                        print("get contract ID")
                        print(Networking_contract_id)
                        Req_flag[2] = 1
        if(Req_flag[0]==1 and Req_flag[1]==1 and Req_flag[2]==1):#必要情報が集まった場合
            break #接続ループを削除
    
    #スマートコントラクト利用設定
    NCI_C = w3.toChecksumAddress(Networking_contract_id)
    #contract_instance = w3.eth.contract(abi=abi, address=NCI_C)
    contract_instance = w3.eth.contract(abi=abi, address=NCI_C)
    #ルータの登録
    print("regist_router")
    tx = contract_instance.functions.regist_router(my_ip_addr).build_transaction({
        "from": myAddr,
        "nonce": w3.eth.getTransactionCount(myAddr),
        "gas": 1728712,
        "gasPrice": w3.toWei("21", "gwei")
    })
    signed_tx = w3.eth.account.sign_transaction(tx, privatekey)
    tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    my_router_id = contract_instance.functions.show_router().call({"from": myAddr})
    print("myrouter_ID:" + str(my_router_id))

    neighbor_array = contract_instance.functions.show_networks().call()
    print("neighbor_array: {}".format(neighbor_array))
    registed_router_num = len(neighbor_array)#登録済みルータ数(自分も入れる)

    #隣接リストの登録
    neighbor_list = make_neighbor(connection_target=connection_target, registed_router_num=registed_router_num)
    tx = contract_instance.functions.regist_neigbor(neighbor_list).build_transaction({
        "from": myAddr,
        "nonce": w3.eth.getTransactionCount(myAddr),
        "gas": 1728712,
        "gasPrice": w3.toWei("21", "gwei")
    })
    signed_tx = w3.eth.account.signTransaction(tx, privatekey)
    tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    #コンテンツ呼び出し
    content_array = contract_instance.functions.show_contents().call()
    print("content_array: {}".format(content_array))
    #registed_content_num = len(content_array)#登録済みコンテンツ数
    #コンテンツ3の登録(FIBは作らない)
    key = ["Router1", "include", "movie"]
    regist_id = [my_router_id]
    tx = contract_instance.functions.regist_content("content3", regist_id, key, False).buildTransaction({
        'from': myAddr,
        'nonce': w3.eth.getTransactionCount(myAddr),
        'gas': 1728712,
        'gasPrice': w3.toWei('21', 'gwei')
    })
    signed_tx = w3.eth.account.signTransaction(tx, privatekey)
    tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    handle.register("ccnx:/content3")#Interest受信用

    sender = contract_instance.functions.return_sender().call({"from": myAddr})
    print("sender")
    print(sender)
    nowID = contract_instance.functions.return_nowID().call()
    print("nowID: " + str(nowID))
    ip_addr_list = contract_instance.functions.return_ipadd().call({"from": myAddr})
    print("IPaddlist")
    print(ip_addr_list)
    registed_content_num = 0




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
                    
                else:
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
                        Req_flag[0] = 1
                        handle.register(helloPrefix)
                    elif func_array[1] in info.name:
                        abi = info.payload
                        print("get abi")
                        print(abi)
                        Req_flag[1] = 1
                    elif func_array[2] in info.name:
                        Networking_contract_id = info.payload
                        print("get contract ID")
                        print(Networking_contract_id)
                        Req_flag[2] = 1
                            



        end_time = time.time()
        elapsed_time = end_time - start_time
        contract_instance = w3.eth.contract(abi=abi, address=Networking_contract_id)
        if(elapsed_time > 60):#60秒立ったら
            content_array = contract_instance.functions.show_contents().call()
            neighbor_array = contract_instance.functions.show_networks().call()
            networks = contract_instance.functions.show_networks().call()
            ip_addr_list = contract_instance.functions.return_ipadd().call()
            print("content_array: {}".format(content_array))
            print("neigbor_array: {}".format(neighbor_array))
            print("networks: {}".format(networks))
            print("IP_addr_list: {}".format(ip_addr_list))
            make_FIB(neighbor_array, myrouterID=my_router_id, content_array=content_array, IP_addr=ip_addr_list, registed_num=registed_content_num)
            registed_content_num = len(content_array)
            registed_router_num = len(neighbor_array)#登録済みルータ数
            neighbor_array = make_neighbor(connection_target=connection_target, registed_router_num=registed_router_num)
            tx = contract_instance.functions.regist_neigbor(neighbor_list).build_transaction({
                "from": myAddr,
                "nonce": w3.eth.getTransactionCount(myAddr),
                "gas": 1728712,
                "gasPrice": w3.toWei("21", "gwei")
            })
            signed_tx = w3.eth.account.signTransaction(tx, privatekey)
            tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            start_time = end_time #現在時間から計測




