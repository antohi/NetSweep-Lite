import socket
import netifaces
import logging

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
        try:
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        dns_servers.append(line.split()[1])
                if dns_servers:
                    logging.info("[SUCCESS] Found DNS servers: " + ", ".join(dns_servers))
                    return dns_servers
                else:
                    logging.warning("[WARNING] No DNS servers found")
                    return "No DNS servers found"
        except IOError:
            logging.error("[EXCEPTION] Could not open /etc/resolv.conf")
            return "[ERROR] IOError"








