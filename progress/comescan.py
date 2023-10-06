import scapy.all as scapy

def packet_handler(packet):
    if packet.haslayer(scapy.TCP) and packet[scapy.TCP].dport == 50000:
        # パケットがTCPプロトコルで宛先ポート番号が50000の場合
        print(packet.show())

# パケットキャプチャを開始
scapy.sniff(filter="port 50000", prn=packet_handler)
