import logging
import subprocess
import socket
import ifaddr
import platform
from datetime import datetime


class NetworkInfo:
    logging.basicConfig(filename="net_log.txt", level = logging.INFO)

    # Detects OS user is using and then pings requested addresses.
    # Tells success of the ping based on the returncode.
    def ping_global(self, addresses):
        result = "ERROR!"
        for ip in addresses:
            ping_cmd = ['ping', '-c', '1', ip] if platform.system() == 'Windows' else ['ping', '-c', '1', ip]
            p = subprocess.run(ping_cmd)
            if p.returncode == 0:
                result = (f"{ip} is up")
            else:
                result = (f"{ip} is down")
        logging.info(f"\n{datetime.now()}: Ping result: {result}")


    def get_socket(self):
        socket_ip = (socket.gethostbyname(socket.gethostname())) # Gets local IP address
        logging.info(f"\n{datetime.now()}: Socket IP: {socket_ip}")
        return socket_ip


    def get_default_gateway(self):
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            if adapter.nice_name == 'en0':
                dg = adapter.ips[1].ip # Returns default gateway IP address
                logging.info(f"\n{datetime.now()}: Default Gateway: {dg}")
                return dg

    def get_dns_nameservers(self):
        with open("/etc/resolv.conf") as f:
            for line in f:
                if line.startswith("nameserver"):
                    line = line.split(" ")
                    dns = line[1]
                    logging.info(f"\n{datetime.now()}: DNS: {dns}")
                    return dns








