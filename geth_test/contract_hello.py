import json
from web3 import Web3
from solcx import compile_source, install_solc
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

# Solidity のソースをコンパイル 文章を生成するようにすればいけそう?
install_solc("0.5.16")
compiled_sol = compile_source(
    '''
    pragma solidity >=0.5.16;

    contract Greeter {
	string public greeting;

	constructor() public {
	    greeting = 'Hello';
	}

	function greet() view public returns (string memory) {
	    return greeting;
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

tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction) #トランザクションの送信

print(w3.toHex(tx_hash)) #トランザクションIDの取得

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash) #生成されたコントラクトアドレスの取得(マイニングしてないと進まない)
print("Contract Deployed At:", tx_receipt['contractAddress'])


