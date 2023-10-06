from scapy.all import *

# 送信元IPアドレスとポート
src_ip = "127.0.0.1"
src_port = 12345

# 送信先IPアドレスとポート
dst_ip = "10.0.0.8"
dst_port = 30303

# TCPパケットを作成
tcp_packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port) / "Hello, TCP!"

# パケットを送信
send(tcp_packet)
