import subprocess
import socket
import ifaddr


class NetworkUptime:

    def ping_global(self, addresses):
        for ip in addresses:
            p = subprocess.run(['ping', '-c', '1', ip])
            if p.returncode == 0:
                print(f"{ip} is up")
            else:
                print(f"{ip} is down")

    def get_socket(self):
        return(socket.gethostbyname(socket.gethostname())) # Gets local IP address

    def get_default_gateway(self):
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            if adapter.nice_name == 'en0':
                return(adapter.ips[1].ip) #Returns default gateway IP address








