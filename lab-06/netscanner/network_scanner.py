import requests
from scapy.all import ARP, Ether, srp

def local_network_scan(ip_range):
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp  

    result = srp(packet, timeout=3, verbose=1)[0]  # Bật debug

    devices = []
    for sent, received in result:
        devices.append({
            'ip': received.psrc,
            'mac': received.hwsrc,
            'vendor': "Unknown"  # Tắt API để kiểm tra trước
        })
    return devices

def main():
    ip_range = "10.14.0.1/16"  # Cập nhật dải mạng
    devices = local_network_scan(ip_range)

    print("Devices on the local network:")
    for device in devices:
        print(f"IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}")

if __name__ == "__main__":
    main()
