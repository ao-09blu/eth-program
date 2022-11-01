from eth_account import Account
from transformers import DATA2VEC_AUDIO_PRETRAINED_MODEL_ARCHIVE_LIST
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
D_account_num = 1

#イーサリアムに接続
w3 = Web3(web3.HTTPProvider("http://localhost:8101"))

#自身のアドレス設定と鍵の入手
myAddr = w3.eth.accounts[my_Account_num]
myAddr_C = w3.toChecksumAddress(myAddr)

privatekey = get_private_key(myAddr_C, Pass_word)
print(privatekey)

nonce = w3.eth.getTransactionCount(my_Account_num)#送信元のnonceのセット

#送信先情報取得
D_addr = w3.toChecksumAddress(w3.eth.accounts[D_account_num])

#トランザクション生成
tx = {
    'chainId': 20,
    'nonce': nonce,
    'to': D_addr,
    'value': w3.toWei(10, "ether"),
    'gas': 2000000,
    'gasPrice': w3.toWei('50', 'gwei'),
}


signed_tx =w3.eth.account.signTransaction(tx, privatekey) #privatekeyで署名

tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction) #トランザクションの送信

print(w3.toHex(tx_hash)) #トランザクションIDの取得


