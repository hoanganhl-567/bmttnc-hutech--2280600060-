from scapy.all import sniff, IP, ICMP

def packet_callback(packet):
    if packet.haslayer(ICMP):
        icmp_packet = packet[ICMP]  # Lấy lớp ICMP từ gói tin

        print("📡 ICMP Packet Information:")
        print(f"🔹 Source IP: {packet[IP].src}")
        print(f"🔹 Destination IP: {packet[IP].dst}")
        print(f"🔹 Type: {icmp_packet.type}")
        print(f"🔹 Code: {icmp_packet.code}")

        # Một số gói ICMP có thể không có ID và Sequence, cần kiểm tra trước khi truy xuất
        if hasattr(icmp_packet, 'id'):
            print(f"🔹 ID: {icmp_packet.id}")

        if hasattr(icmp_packet, 'seq'):
            print(f"🔹 Sequence: {icmp_packet.seq}")

        if hasattr(icmp_packet, 'load'):
            print(f"🔹 Load: {icmp_packet.load}")

        print("=" * 50)

def main():
    print("🚀 Listening for ICMP packets... (Press Ctrl+C to stop)")
    sniff(prn=packet_callback, filter="icmp", store=0)

if __name__ == "__main__":
    main()
