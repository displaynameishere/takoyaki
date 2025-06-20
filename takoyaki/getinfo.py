import platform
import os
import json
import socket
import datetime
import shutil
import sys

def get_cpu_model():
    cpu = platform.processor()
    if cpu:
        return cpu
    if sys.platform.startswith("linux"):
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        return line.split(":", 1)[1].strip()
        except Exception:
            pass
    return "Unknown"

def get_total_ram():
    if sys.platform == "linux" or sys.platform == "linux2":
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        parts = line.split()
                        # kB to GB
                        return round(int(parts[1]) / 1024 / 1024, 2)
        except Exception:
            pass
    elif sys.platform == "darwin":
        try:
            import subprocess
            out = subprocess.check_output(["sysctl", "hw.memsize"]).decode()
            val = int(out.strip().split(":")[1])
            return round(val / (1024 ** 3), 2)
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            return round(stat.ullTotalPhys / (1024 ** 3), 2)
        except Exception:
            pass
    return None

def get_disk_size_gb(path="/"):
    try:
        total, used, free = shutil.disk_usage(path)
        return round(total / (1024**3), 2)
    except Exception:
        return None

def get_ip_addresses():
    ips = []
    try:
        hostname = socket.gethostname()
        ips.append(socket.gethostbyname(hostname))
    except Exception:
        pass
    # prob will miss interfaces, but trying to keep it dependency free for now
    return ips

def get_device_fingerprint():
    uname = platform.uname()
    hostname = socket.gethostname()
    cpu_count = os.cpu_count() or 1

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
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    return hostname, device_info

def read_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def write_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
