from scapy.all import *

IPadd = "192.168.72.128"
TCPport = 30303

# フィルタリング関数
def packet_filter(packet):
    # 特定のポートからのパケットをフィルタリング
    if IP in packet and  packet[IP].src == IPadd and packet[TCP].sport == TCPport:
        print("Captured Packet:")
        print(packet.show())

        #パケットをブロックする条件
        if condition_to_block_packet(packet):
            print("Blocking Packet")
            return

def condition_to_block_packet(packet):
    print("I want to reject")
    return False

# パケットキャプチャを開始
packets = sniff(filter="src host 192.168.72.128 and tcp port 30303", prn=lambda x: x.summary(), lfilter=packet_filter)

# パケットを確認して送信しないように制御
for packet in packets:
    # パケットの内容を表示
    print(packet.summary())

    # パケットを相手に送信しない条件を設定
    if condition_to_block_packet(packet):
        continue

    # パケットを相手に送信
    sendp(packet, iface='your_network_interface')  # ネットワークインターフェースを指定して送信
