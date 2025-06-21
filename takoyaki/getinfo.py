import psutil
import platform
import socket
import datetime
import json
import os
import shutil
import pytz
import sys

def get_cpu_model():
    try:
        if sys.platform.startswith("linux") or sys.platform.startswith("darwin"):
            return platform.processor()
        if sys.platform == "win32":
            return psutil.cpu_info().brand
    except Exception as e:
        return f"Error fetching CPU model: {e}"

def get_total_ram():
    try:
        return round(psutil.virtual_memory().total / (1024 ** 3), 2)
    except Exception as e:
        return f"Error fetching RAM: {e}"

def get_disk_size_gb(path="/"):
    try:
        total, used, free = shutil.disk_usage(path)
        return round(total / (1024**3), 2)
    except Exception as e:
        return f"Error fetching disk size: {e}"

def get_ip_addresses():
    try:
        ips = []
        addrs = psutil.net_if_addrs()
        for interface, snics in addrs.items():
            for snic in snics:
                if snic.family == socket.AF_INET:
                    ips.append(snic.address)
        if not ips:
            ips.append(socket.gethostbyname(socket.gethostname()))
        return ips
    except Exception as e:
        return [f"Error fetching IPs: {e}"]

def get_device_fingerprint():
    try:
        uname = platform.uname()
        hostname = socket.gethostname()
        cpu_count = psutil.cpu_count(logical=True)

        device_info = {
            "hostname": hostname,
            "system": uname.system,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine,
            "cpu": {
                "model": get_cpu_model(),
                "cores": cpu_count
            },
            "memory_gb": get_total_ram(),
            "disk_gb": get_disk_size_gb(),
            "ip_addresses": get_ip_addresses(),
            "timestamp": datetime.datetime.now(pytz.utc).isoformat()
        }
        return hostname, device_info
    except Exception as e:
        return "Error", {"error": str(e)}

def read_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return {"error": f"Error reading JSON file: {e}"}

def write_json(filename, data):
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        return f"Error writing JSON file: {e}"

if __name__ == "__main__":
    hostname, device_info = get_device_fingerprint()
    print(json.dumps(device_info, indent=4))
