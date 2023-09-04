from scapy.all import *

def packet_handler(packet):
    if IP in packet and packet[IP].src == "192.168.72.128" and TCP in packet and packet[TCP].sport == 30303:
        print ("Captured Packt:")
        print(packet.show())

sniff(filter="src host 192.168.72.128 and tcp port 30303", prn=packet_handler)

