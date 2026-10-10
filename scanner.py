import re
import socket
import subprocess


def get_arp_output():
    """Run the Windows 'arp -a' command and return the text it prints."""
    result = subprocess.run(["arp", "-a"], capture_output=True, text=True)
    return result.stdout


def parse_devices(arp_text):
    """Find every IP address and MAC address in the ARP table text."""
    pattern = r"(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]{17})\s+(\w+)"
    devices = []
    for ip, mac, kind in re.findall(pattern, arp_text):
        devices.append({"ip": ip, "mac": mac.lower(), "type": kind})
    return devices


def is_real_device(device):
    """Return False for broadcast and multicast entries, which are not real devices."""
    mac = device["mac"]
    if mac == "ff-ff-ff-ff-ff-ff":
        return False
    if mac.startswith("01-00-5e"):
        return False
    return True


def get_hostname(ip):
    """Ask the network for the name that belongs to an IP address."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except OSError:
        return "unknown"


def print_devices(devices):
    """Print the devices as a table with a count at the bottom."""
    print(f"{'IP address':<18}{'MAC address':<20}{'Name'}")
    print("-" * 60)
    for device in devices:
        print(f"{device['ip']:<18}{device['mac']:<20}{device['name']}")
    print(f"\n{len(devices)} device(s) found")


def main():
    arp_text = get_arp_output()
    all_entries = parse_devices(arp_text)
    real_devices = []
    for device in all_entries:
        if is_real_device(device):
            device["name"] = get_hostname(device["ip"])
            real_devices.append(device)
    print_devices(real_devices)


if __name__ == "__main__":
    main()