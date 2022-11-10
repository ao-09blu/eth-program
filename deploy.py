# 1. Import Module
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# 2. Access Ganache local server
web3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
print(web3.isConnected())

# 3. Account Address, private key
key = "002d339b02006031e2928c662c062916403206ad944cb0f5311a219c80bf3a42"
acct = web3.eth.account.privateKeyToAccount(key)

# 4. Set smart contract information
truffleFile = json.load(open('greeter/build/contracts/greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']
contract= web3.eth.contract(bytecode=bytecode, abi=abi)

# 5. Building transaction information
construct_txn = contract.constructor().buildTransaction({
    'from': acct.address,
    'nonce': web3.eth.getTransactionCount(acct.address),
    'chainId': 1337,
    'gasPrice': web3.eth.gas_price})

# 6. Send Transaction
signed  = acct.signTransaction(construct_txn)
tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())

# 7. Display contract address
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])