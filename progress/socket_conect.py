import os
import json
import socket

IPC_PATH = './node19/geth.ipc'  # 実際のIPCファイルのパス

def geth_ipc_socket_connect(ipc_path):
    client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client_socket.connect(ipc_path)
    return client_socket

def receive_data(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    return data

if __name__ == '__main__':
    if os.path.exists(IPC_PATH):
        ipc_socket = geth_ipc_socket_connect(IPC_PATH)
        print("Connected to Geth IPC socket.")

        try:
            while True:
                data = receive_data(ipc_socket)
                if data:
                    parsed_data = json.loads(data)
                    print("Received data:", parsed_data)
                else:
                    print("No data received.")
        except KeyboardInterrupt:
            print("Exiting...")
            ipc_socket.close()
    else:
        print("IPC file not found.")