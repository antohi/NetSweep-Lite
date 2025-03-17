import socket
import ifaddr

class NetworkInfo:
    def get_socket(self):
        socket_ip = (socket.gethostbyname(socket.gethostname())) # Gets local IP address
        return socket_ip


    def get_default_gateway(self):
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            if adapter.nice_name == 'en0':
                dg = adapter.ips[1].ip # Returns default gateway IP address
                return dg

    def get_dns_nameservers(self):
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    line = line.split(" ")
                    dns = line[1]
                    return dns








