from web3 import Web3

#接続
w3 = Web3(Web3.HTTPProvider("http://localhost:8101"))

#ABI
abi =[{'inputs': [], 'payable': False, 'stateMutability': 'nonpayable', 'type': 'constructor'}, {'constant': True, 'inputs': [], 'name': 'greet', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}, {'constant': True, 'inputs': [], 'name': 'greeting', 'outputs': [{'internalType': 'string', 'name': '', 'type': 'string'}], 'payable': False, 'stateMutability': 'view', 'type': 'function'}]

#コントラクトアドレス
contractAddress = '0xfe7B44A02E1944e71256875cb334F32e0Fc137Eb'

#コントラクトオブジェクト
greeter = w3.eth.contract(address=contractAddress, abi=abi)

#呼び出しと表示
print(greeter.functions.greet().call())