import csv
import re
import socket
import subprocess
from datetime import datetime
from pathlib import Path

HISTORY_FILE = Path(__file__).parent / "scan_history.csv"


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


def load_known_macs():
    """Read the MAC addresses that earlier scans saved to the history file."""
    known = set()
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, newline="") as file:
            for row in csv.DictReader(file):
                known.add(row["mac"])
    return known


def save_scan(devices):
    """Add this scan's devices to the history file, with the time of the scan."""
    file_is_new = not HISTORY_FILE.exists()
    scan_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(HISTORY_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if file_is_new:
            writer.writerow(["time", "ip", "mac", "name"])
        for device in devices:
            writer.writerow([scan_time, device["ip"], device["mac"], device["name"]])


def print_devices(devices):
    """Print the devices as a table, marking any that were not seen before."""
    print(f"{'IP address':<18}{'MAC address':<20}{'Name':<24}{'Status'}")
    print("-" * 68)
    new_count = 0
    for device in devices:
        status = ""
        if device["new"]:
            status = "NEW"
            new_count += 1
        print(f"{device['ip']:<18}{device['mac']:<20}{device['name']:<24}{status}")
    print(f"\n{len(devices)} device(s) found, {new_count} new since earlier scans")


def main():
    known_macs = load_known_macs()
    arp_text = get_arp_output()
    all_entries = parse_devices(arp_text)
    real_devices = []
    for device in all_entries:
        if is_real_device(device):
            device["name"] = get_hostname(device["ip"])
            device["new"] = device["mac"] not in known_macs
            real_devices.append(device)
    print_devices(real_devices)
    save_scan(real_devices)


if __name__ == "__main__":
    main()