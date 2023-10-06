import socket
import struct

def capture_packets(port):
    try:
        # パケットソケットを作成
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
        
        while True:
            # パケットを受信
            packet = s.recvfrom(65535)
            ethernet_header = packet[0][:14]
            ip_header = packet[0][14:34]
            tcp_header = packet[0][34:54]
            data = packet[0][54:]
            
            # IPヘッダから送信元と宛先IPアドレスを取得
            ip_header_data = struct.unpack("!BBHHHBBH4s4s", ip_header)
            source_ip = socket.inet_ntoa(ip_header_data[8])
            dest_ip = socket.inet_ntoa(ip_header_data[9])
            
            # TCPヘッダからデータオフセットを取得 (データオフセットの値は上位4ビット)
            tcp_data_offset = (struct.unpack("!B", tcp_header[12:13])[0] >> 4) * 4
            
            # TCPヘッダから送信元ポートと宛先ポートを取得
            source_port, dest_port = struct.unpack("!HH", tcp_header[:4])
            
            # 送信元ポートが30303である場合のみ表示
            if source_port == port:
                print(f"Captured Packet from {source_ip}:{source_port} to {dest_ip}:{dest_port}")
                print("Packet Data:")
                print(data[tcp_data_offset:].hex())
    
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    port = 30303  # キャプチャしたいポート番号を指定
    capture_packets(port)

