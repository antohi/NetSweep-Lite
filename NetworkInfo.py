import socket
import netifaces

class NetworkInfo:
    def get_socket(self):
        socket_ip = (socket.gethostbyname(socket.gethostname())) # Gets local IP address
        return socket_ip


    def get_default_gateway(self):
        gateways = netifaces.gateways()
        if netifaces.AF_INET in gateways['default']:
            return gateways['default'][netifaces.AF_INET][0]  # IPv4 Gateway
        return "N/A"

    def get_dns_nameservers(self):
        dns_servers = []
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    dns_servers.append(line.split()[1])
        return dns_servers if dns_servers else "N/A"








