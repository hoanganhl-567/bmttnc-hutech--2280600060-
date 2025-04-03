import requests
from scapy.all import ARP, Ether, srp

def get_vendor(mac_address):
    """Tra cứu nhà sản xuất từ địa chỉ MAC."""
    try:
        url = f"https://api.macvendors.com/{mac_address}"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return "Unknown"

def local_network_scan(ip_range):
    """Quét mạng cục bộ để tìm các thiết bị."""
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp  

    result = srp(packet, timeout=5, verbose=False)[0]
    devices = []
    for sent, received in result:
        mac = received.hwsrc
        vendor = get_vendor(mac)  # Lấy tên Vendor từ MAC Address
        devices.append({
            'ip': received.psrc,
            'mac': mac,
            'vendor': vendor
        })
    return devices

def main():
    ip_range = "192.168.1.1/24"  # Đảm bảo IP đúng với mạng của bạn
    devices = local_network_scan(ip_range)

    if devices:
        print("Devices on the local network:")
        for device in devices:
            print(f"IP: {device['ip']}, MAC: {device['mac']}, Vendor: {device['vendor']}")
    else:
        print("No devices found or no responses received.")

if __name__ == "__main__":
    main()
