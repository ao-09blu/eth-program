# 1. Import Module
import json
from web3 import Web3
import re


def make_private_key(P_key):
    key_array = re.findall("\d+",P_key)#keyの中身を配列に格納
    privatekey = ""
    for i in range(len(key_array)):
        key_array[i] = format(int(key_array[i]), 'x')
        privatekey += key_array[i].zfill(2)
    return privatekey


# 2. Access Ganache local server
ganache_url = "http://192.168.72.128:8101"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# 3. Account Address, private key
account_0   = web3.toChecksumAddress('0x094878476afa2d977f8ee35a71b3a821f95de909') # Input selected Address

account_1   = web3.toChecksumAddress('0x5f8faebacef8c03fa0e48c82559c0a0ab054c7a9') # Input selected Address

P_key="187 224 155 157 113 243 134 8 122 44 113 56 221 55 169 236 176 142 215 119 40 34 34 86 151 159 152 43 7 169 141 231"
privatekey = make_private_key(P_key)
# 4. Get nonce value
nonce = web3.eth.getTransactionCount(account_0)

# 5. Transaction data
tx = {
    'from': account_0,
    'nonce': nonce,
    'to': account_1,
    'value': web3.toWei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
}

# 6. Generate singed transaction data
signed_tx = web3.eth.account.signTransaction(tx, privatekey)

# 7. Ethereum Transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# 8. Check Transaction address
print(web3.toHex(tx_hash))
