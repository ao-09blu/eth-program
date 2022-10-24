# 1. Import Module
import json
from web3 import Web3

# 2. Access Ganache local server
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# 3. Account Address, private key
account_0   = '0x2d0D39cE57db38C52F37B53204e6B6C4245F69e4' # Input selected Address
account_1   = '0x9ab8b7B8d9e7B98d60D7D976839B16F2cC063F1a' # Input selected Address
private_key = '1392129fc3ee7a1f1023850cce891b83de27f8dba6720d99e0beb6557e260690' # Input selected Address's private key

# 4. Get nonce value
nonce = web3.eth.getTransactionCount(account_0)

# 5. Transaction data
tx = {
    'nonce': nonce,
    'to': account_1,
    'value': web3.toWei(1, 'ether'),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei'),
}

# 6. Generate singed transaction data
signed_tx = web3.eth.account.signTransaction(tx, private_key)

# 7. Ethereum Transaction
tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

# 8. Check Transaction address
print(web3.toHex(tx_hash))
