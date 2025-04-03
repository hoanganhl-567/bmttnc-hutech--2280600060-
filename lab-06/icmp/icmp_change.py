from scapy.all import sniff, send, IP, ICMP

def modify_icmp_packet(packet):
    if packet.haslayer(ICMP):
        icmp_packet = packet[ICMP]

        print("📡 Original ICMP Packet:")
        print(f"🔹 Source IP: {packet[IP].src}")
        print(f"🔹 Destination IP: {packet[IP].dst}")
        print(f"🔹 Type: {icmp_packet.type}")
        print(f"🔹 Code: {icmp_packet.code}")

        if hasattr(icmp_packet, 'id'):
            print(f"🔹 ID: {icmp_packet.id}")

        if hasattr(icmp_packet, 'seq'):
            print(f"🔹 Sequence: {icmp_packet.seq}")

        if hasattr(icmp_packet, 'load'):
            print(f"🔹 Load: {bytes(icmp_packet.load)}")  # Hiển thị load dưới dạng byte

        # Tạo gói ICMP mới với nội dung thay đổi
        new_load = b"This is a modified ICMP packet."
        new_packet = IP(src=packet[IP].dst, dst=packet[IP].src) / \
                     ICMP(type=icmp_packet.type, code=icmp_packet.code, id=icmp_packet.id, seq=icmp_packet.seq) / \
                     new_load

        print("\n📡 Modified ICMP Packet:")
        print(f"🔹 Source IP: {new_packet[IP].src}")
        print(f"🔹 Destination IP: {new_packet[IP].dst}")
        print(f"🔹 Type: {new_packet[ICMP].type}")  # Truy cập từ lớp ICMP
        print(f"🔹 Code: {new_packet[ICMP].code}")

        if hasattr(new_packet[ICMP], 'id'):
            print(f"🔹 ID: {new_packet[ICMP].id}")

        if hasattr(new_packet[ICMP], 'seq'):
            print(f"🔹 Sequence: {new_packet[ICMP].seq}")

        if hasattr(new_packet, 'load'):
            print(f"🔹 Load: {bytes(new_packet[ICMP].payload)}")  # Hiển thị payload mới

        print("=" * 50)

        send(new_packet)  # Gửi gói tin đã chỉnh sửa

def main():
    print("🚀 Listening for ICMP packets... (Press Ctrl+C to stop)")
    sniff(prn=modify_icmp_packet, filter="icmp", store=0)

if __name__ == "__main__":
    main()
