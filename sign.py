# 1. Import Module
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# 2. Access Ganache local server
web3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
print(web3.isConnected())

# 3. Account Address, private key
key  = "4f3fd3f5656d065f2a396d547420d7f03e4117f5bdecf364e5e90c7248bbfd05"
acct = web3.eth.account.privateKeyToAccount(key)

# 4. Get smart contract information
truffleFile = json.load(open('greeter/build/contracts/greeter.json'))
abi         = truffleFile['abi']
bytecode    = truffleFile['bytecode']

# 5. Set contract address
contract_address = "0xb70E94e46f6F712C0D51E2bce68cAf04c08DD464"
contract_address = Web3.toChecksumAddress(contract_address) #modify

# 6. Instantiate and deploy contract
contract = web3.eth.contract(abi=abi, bytecode=bytecode)
contract_instance = web3.eth.contract(abi=abi, address=contract_address)
greeting = "Hello all  my goody people nonce"
tx = contract_instance.functions.greet(greeting).buildTransaction({'nonce': web3.eth.getTransactionCount(acct.address)})

# 7. Send transaction , and get tx receipt to get contract address
signed_tx = web3.eth.account.signTransaction(tx, key)
hash= web3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(hash.hex())