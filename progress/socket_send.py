import socket

def receive_packets(port):
    # ソケットを作成
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        # ソケットを指定したポートにバインド
        s.bind(('localhost', port))  # localhostを指定していますが、必要に応じて適切なIPアドレスを指定できます

        print(f"ポート {port} でパケットを受信中...")

        while True:
            data, addr = s.recvfrom(1024)  # 1024バイトまでのデータを受信
            print(f"受信したパケット: {data.decode()}")

if __name__ == "__main__":
    target_port = 12345  # パケットを受信するポート番号を指定
    receive_packets(target_port)
