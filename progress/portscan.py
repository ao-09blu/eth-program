import socket

def main():
    host = "0.0.0.0"  # すべてのインターフェースからの接続を受け入れる
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Listening on port {port}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from: {client_address}")
            
            data = client_socket.recv(1024)  # パケットの最大サイズ
            if data:
                print(f"Received data:\n{data.decode('utf-8')}")
            
            client_socket.close()
    except KeyboardInterrupt:
        print("Server stopped.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
