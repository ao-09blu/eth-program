import socket

# リスニングするホストとポート
HOST = '127.0.0.1'  # ローカルホスト
PORT = 50000

# ソケットを作成し、指定のホストとポートでリスニング
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Listening on {HOST}:{PORT}...")

    while True:
        # クライアントからの接続を待機
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        with client_socket:
            # リダイレクトされたパケットを受信
            packet = client_socket.recv(65535)
            
            # 受信したパケットを処理する（ここでは表示）
            print(f"Received packet: {packet}")

