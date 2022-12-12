from web3 import Web3
import subprocess
import re

#接続
w3 = Web3(Web3.HTTPProvider("http://localhost:8101"))

def get_private_key(account_addr_C, Pass):#checksumをしておく
    proc = subprocess.run('node get_key.js '+ account_addr_C + " " +  Pass, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)#jsonファイルとパスワードからkeyを取得
    key_array = re.findall("\d+",proc.stdout.decode('cp932'))#keyの中身を配列に格納
    privatekey = ""
    for i in range(len(key_array)):
        key_array[i] = format(int(key_array[i]), 'x')
        privatekey += key_array[i]
    return privatekey


Pass_word = "2"#自分のパスワード
my_Account_num = int(Pass_word) - 1 #アカウントの番号

#イーサリアムに接続
w3 = Web3(Web3.HTTPProvider("http://localhost:8101"))

#自身のアドレス設定と鍵の入手
myAddr = w3.toChecksumAddress(w3.eth.accounts[my_Account_num])

privatekey = get_private_key(myAddr, Pass_word)

#ABI
abi =[{'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'constant': True, 'inputs': [], 'name': 'greet', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'greeting', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': False, 'inputs': [{'internalType': 'string', 'name': '_greeting', 'type': 'string'}], 'name': 'setGreeting', 'outputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'function'}]

#コントラクトアドレス
contractAddress = '0x28327E8C890f5f136e9D5bF8b35fEEEfAcD2d724'

#コントラクトオブジェクト
greeter = w3.eth.contract(address=contractAddress, abi=abi)

#呼び出しと表示
print(greeter.functions.greet().call())

tx = greeter.functions.setGreeting("Mine").buildTransaction({
    'from': myAddr,
    'nonce': w3.eth.getTransactionCount(myAddr),
    'gas': 1728712,
    'gasPrice': w3.toWei('21', 'gwei')
})

signed_tx = w3.eth.account.signTransaction(tx, privatekey)

#トランザクションの送信
tx_hash =w3.eth.sendRawTransaction(signed_tx.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(greeter.functions.greet().call())