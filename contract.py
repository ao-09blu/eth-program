# 1. Import Module
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# 2. Access Ganache local server
web3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
print(web3.isConnected())

# 3. Account Address, private key
key = "3f59f3d5fcee72154cfdff3757a528ad87cc14af6b39b48815f8c70a51ada837"
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
    'gas': 1728712,
    'gasPrice': web3.toWei('30', 'gwei')})

print(construct_txn)

# 6. Send Transaction
signed  = acct.signTransaction(construct_txn)
tx_hash = web3.eth.sendRawTransaction(signed.rawTransaction)
print(tx_hash.hex())

# 7. Display contract address
tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
print("Contract Deployed At:", tx_receipt['contractAddress'])



contract_address = tx_receipt['contractAddress']
contract_address = Web3.toChecksumAddress(contract_address) #modify

# 6. Instantiate and deploy contract
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
contract_instance = web3.eth.contract(abi=abi, address=contract_address)
greeting = "Hello!!"
print("correct word=" + greeting)
tx = contract_instance.functions.greet(greeting).buildTransaction({'nonce': web3.eth.getTransactionCount(acct.address)})

# 7. Send transaction , and get tx receipt to get contract address
signed_tx = web3.eth.account.signTransaction(tx, key)
hash= web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(hash.hex())


# 6. Read Contract function
contract_instance = web3.eth.contract(abi=abi, address=contract_address)
print('Contract value: {}'.format(contract_instance.functions.getGreeting().call()))