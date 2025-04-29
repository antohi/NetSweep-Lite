import socket
import netifaces
import logging
import platform
import os

class NetworkInfo:
    def get_socket(self):
        socket_ip = (socket.gethostbyname(socket.gethostname())) # Gets local IP address
        logging.info(f"[LOCAL IP] {socket_ip}")
        return f"[LOCAL IP] {socket_ip}"


    def get_default_gateway(self):
        gateways = netifaces.gateways()
        if netifaces.AF_INET in gateways['default']:
            logging.info(f"[GATEWAY] {gateways['default'][netifaces.AF_INET][0]}")
            return f"[GATEWAY] {gateways['default'][netifaces.AF_INET][0]}"  # IPv4 Gateway
        return "[GATEWAY ERROR]"

    def get_dns_nameservers(self):
        dns_servers = []
        try:
            with open("/etc/resolv.conf") as f:
                for line in f:
                    if line.startswith("nameserver"):
                        dns_servers.append(line.split()[1])
                if dns_servers:
                    logging.info("[DNS SERVERS] " + ", ".join(dns_servers))
                    return "[DNS SERVERS] " + ", ".join(dns_servers)
                else:
                    logging.warning("[WARNING] No DNS servers found")
                    return "No DNS servers found"
        except IOError:
            logging.error("[EXCEPTION] Could not open /etc/resolv.conf")
            return "[ERROR] IOError"

    def get_sys_info(self):
        logging.info("\n===SYSTEM/NETWORK INFO===")
        logging.info(f"[PLATFORM] {platform.platform()}")
        logging.info(f"[CPU] {platform.machine()}")
        logging.info(f"[USER] {os.getlogin()}")








