from rsa import PrivateKey, sign
from web3 import Web3
from solcx import compile_source
import web3
import subprocess
import re


#イーサリアムに接続
w3 = Web3(web3.HTTPProvider("http://localhost:8101"))

#自分のアドレス
account_1 = w3.toChecksumAddress('0x0b05fc1720fd4789f9245373e9c6e1f94e53183b')
#account_2 = w3.toChecksumAddress('0xe533d8b23a1e70177cb09167e7b098db1fd1136f')

#自分のパスワード
Pass_word = "1"

#自分の秘密鍵
proc = subprocess.run('node get_key.js '+ account_1 + " " +  Pass_word, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

key_array = re.findall("\d+",proc.stdout.decode('cp932'))

privatekey = ""
for i in range(len(key_array)):
    key_array[i] = format(int(key_array[i]), 'x')
    privatekey += key_array[i]
print(privatekey)

nonce = w3.eth.getTransactionCount(account_1)

tx = {
    'chainId': 20,
    'nonce': nonce,
    'to': account_1,
    'value': w3.toWei(10, "ether"),
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
}

signed_tx =w3.eth.account.signTransaction(tx, privatekey)

tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)

print(w3.toHex(tx_hash))


