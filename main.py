import argparse
import csv
import time
import pycurl
import netifaces as ni
import ipaddress
from os import getenv
from io import BytesIO


def find_local_interface_with_ips():
    for interface in ni.interfaces():
        addrs = ni.ifaddresses(interface)
        if ni.AF_INET in addrs and len(addrs[ni.AF_INET]) > 1:
            return interface
    return None


def get_local_ips(interface):
    addrs = ni.ifaddresses(interface)
    disallowed_networks = getenv("DISALLOWED_NETWORKS", "192.168.0.0/16,172.17.0.0/16").split(",")

    disallowed = []
    allowed = []
    for iprange in disallowed_networks:
        for ip in ipaddress.ip_network(iprange, strict=False):
            disallowed.append(ip)
    for addr_info in addrs[ni.AF_INET]:
        if ipaddress.IPv4Address(addr_info['addr']) not in disallowed:
            allowed.append(addr_info['addr'])
    return allowed


def get_public_ip(local_ip):
    buffer = BytesIO()

    c = pycurl.Curl()
    c.setopt(c.URL, "http://icanhazip.com")
    c.setopt(c.WRITEDATA, buffer)
    c.setopt(c.CONNECTTIMEOUT, 5)
    c.setopt(pycurl.INTERFACE, local_ip)
    c.setopt(c.TIMEOUT, 10)

    try:
        c.perform()
        public_ip = buffer.getvalue().decode().strip()
        return public_ip
    except pycurl.error as e:
        print(f"Error getting public IP for {local_ip}: {str(e)}")
        return None
    finally:
        c.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='IP collection script.')
    parser.add_argument('-t', '--time', type=int, nargs='+', default=[1, 3, 12, 24],
                        help='Time intervals for IP collection in hours.')
    args = parser.parse_args()

    local_interface = find_local_interface_with_ips()
    if local_interface is None:
        raise Exception("No interface with multiple IP addresses found")

    local_ips = get_local_ips(local_interface)

    ip_dict = {}
    for local_ip in local_ips:
        ip_dict[local_ip] = {"Public IP": get_public_ip(local_ip)}

    for interval in args.time:
        time.sleep(interval * 60 * 60)
        for local_ip in local_ips:
            ip_dict[local_ip][f"Public IP (after {interval} hour)"] = get_public_ip(local_ip)

    with open("ip_collection.csv", "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Local IP", "Public IP"] + [f"Public IP (after {interval} hour)" for interval in args.time] + ["IP Changed"])
        for local_ip, ip_info in ip_dict.items():
            public_ip = ip_info.get("Public IP")
            ip_changed = "True" if any(public_ip != ip for ip in ip_info.values()) else "False"
            csv_writer.writerow([local_ip, public_ip] + [ip_info.get(f"Public IP (after {interval} hour)") for interval in args.time] + [ip_changed])

    print("IP collection completed.")
