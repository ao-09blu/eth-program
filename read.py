# 1. Import Module
import json
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract

# 2. Access Ganache local server
web3 = Web3(HTTPProvider("HTTP://127.0.0.1:7545"))
print(web3.isConnected())

# 4. Get smart contract information
truffleFile = json.load(open('greeter/build/contracts/greeter.json'))
abi = truffleFile['abi']
bytecode = truffleFile['bytecode']

# 5. Set contract address
contract_address = "0xa1364d76bE9F3644c890Fb0c3922df3b42b4E5c1"
contract_address = Web3.toChecksumAddress(contract_address) #modify
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

# 6. Read Contract function
contract_instance = web3.eth.contract(abi=abi, address=contract_address)
print('Contract value: {}'.format(contract_instance.functions.getGreeting().call()))