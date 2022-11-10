import json
from web3 import Web3
from solcx import compile_source
import web3
import subprocess
import re

def get_private_key(account_addr_C, Pass):#checksumをしておく
    proc = subprocess.run('node get_key.js '+ account_addr_C + " " +  Pass, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#jsonファイルとパスワードからkeyを取得
    key_array = re.findall("\d+",proc.stdout.decode('cp932'))#keyの中身を配列に格納
    privatekey = ""
    for i in range(len(key_array)):
        key_array[i] = format(int(key_array[i]), 'x')
        privatekey += key_array[i]
    return privatekey


Pass_word = "1"#自分のパスワード
my_Account_num = int(Pass_word) - 1 #アカウントの番号

#イーサリアムに接続
w3 = Web3(web3.HTTPProvider("http://localhost:8101"))

#自身のアドレス設定と鍵の入手
myAddr = w3.toChecksumAddress(w3.eth.accounts[my_Account_num])

privatekey = get_private_key(myAddr, Pass_word)

truffleFile = json.load(open('./greeter/build/contracts/greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract= w3.eth.contract(bytecode=bytecode, abi=abi)

contract_address = "0xB93aA01Cd0DE1D15DED73FBff98522C927A3d009"
contract_address = w3.toChecksumAddress(contract_address) #modify

# 6. Instantiate and deploy contract
contract = w3.eth.contract(abi=abi, bytecode=bytecode)
contract_instance = w3.eth.contract(abi=abi, address=contract_address)
greeting = "Hello all  my goody people nonce"
tx = contract_instance.functions.greet(greeting).buildTransaction({'nonce': w3.eth.getTransactionCount(myAddr)})#ここで金額指定しないからエラーが起こる?

# 7. Send transaction , and get tx receipt to get contract address
signed_tx = w3.eth.account.signTransaction(tx, privatekey)
hash= w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(hash.hex())