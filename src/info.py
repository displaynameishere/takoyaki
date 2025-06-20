"""File that saves device info"""
import platform
import os
import json



os_model = platform.platform(aliased=True)
name = platform.node()
cpu_cores = os.cpu_count()
cpu_model = platform.processor()


device_info = {
    "hostname": {
    "os":f"{os_model} V{platform.release()}",
    "cpu_info": f"{cpu_model} with {cpu_cores} cores"
    }
}

all_info: dict = json.load(open("d_info.json","+a"))
all_info[name] = device_info
# may not work properly, needs testing
