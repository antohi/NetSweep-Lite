import subprocess
import socket
import struct


class NetworkUptime:
    ip_addresses = []

    def __init__(self, ip_addresses):
        self.ip_addresses = ip_addresses

    def ping_global(self):
        for ip in self.ip_addresses:
            p = subprocess.run(['ping', '-c', '1', ip])
            if p.returncode == 0:
                print(f"{ip} is up")
            else:
                print(f"{ip} is down")

    def get_socket(self):
        print(socket.gethostbyname(socket.gethostname())) # Gets local IP address




