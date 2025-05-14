import subprocess
import platform
import logging
import concurrent.futures
import re
import ipaddress
from colorama import Fore, Style, init


class PingTool:
    def __init__(self):
        self.addresses_to_ping = set([])
        self.results = []

    # Add IPs to the list
    def add_ip(self, ip):
        self.addresses_to_ping.add(ip)

    #Get addys
    def get_addresses(self):
        return self.addresses_to_ping

    #Pings a single IP, plays sound based on success/failure
    def ping_ip(self, ip):
        try:
            ping_cmd = ['ping', '-n', '4', ip] if platform.system() == 'Windows' else ['ping', '-c', '4', ip]
            p = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if p.returncode == 0:
                self.get_detailed_info(str(p), ip)
                logging.info(f"{Fore.GREEN}[SUCCESS]:{Style.RESET_ALL} Ping to {ip} was successful")
 #               playsound('/assets/ding.mp3')
                return  f"{ip} is UP"
            else:
                logging.warning(f"{Fore.RED}[FAIL]: Ping to {ip} was unsuccessful. Return code: {p.returncode}{Style.RESET_ALL}")
#               playsound('/assets/error.mp3')
                return f"{ip} is {Fore.LIGHTRED_EX}DOWN{Style.RESET_ALL}"
        except Exception as e:
            logging.error(f"[EXCEPTION]: {e}" )
            return f"{Fore.RED}[ERROR]{Style.RESET_ALL} {ip} is {Fore.LIGHTRED_EX}DOWN{Style.RESET_ALL}"

    # Concurrently pings all IP addresses
    def ping_addresses(self, addresses):
        # using ThreadPoolExecutor for parallel pinging
        logging.info(f"{Fore.GREEN}===IP PING INFO==={Style.RESET_ALL}")
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.ping_ip, addresses)  # Executes ping_ip for each address in parallel

        # printing results to console
        for result in results:
            print(result)

    # Pings addresses in a range of IPs
    def ping_addresses_in_range(self, start, end):
        logging.info(f"{Fore.GREEN}===RANGE PING INFO==={Style.RESET_ALL}")
        # Converting to IPv4 Objects to easier iteration in for loop
        range_addresses = set([])
        start_ip = ipaddress.IPv4Address(start)
        end_ip = ipaddress.IPv4Address(end)

        for ip in range(int(start_ip), int(end_ip) + 1):
            # Converting back to ip addresses when adding to addresses[]
            range_addresses.add((str(ipaddress.IPv4Address(ip))))
        self.ping_addresses(range_addresses)

    # Extracts latency and packet information
    def get_detailed_info(self, p, ip):
        # Latency info
        logging.info(f"{Fore.GREEN}=LATENCY, PACKET LOSS, PING STATUS INFO={Style.RESET_ALL}")
        latency_info = re.search(r"(\d+\.\d+)/(\d+\.\d+)/(\d+\.\d+)", p)
        min, avg, max = latency_info.groups()
        logging.info(f"{ip} [LATENCY] Minimum: {min}, Average: {avg}, Maximum: {max}")

        # Packet info
        packets_transmitted = re.search(r"(\d) packets transmitted", p)
        packets_received = re.search(r"(\d) packets received", p)
        packets_lost = re.search(r"(\d+\.\d+)% packet loss", p)

        transmitted = packets_transmitted.group(1) if packets_transmitted else "N/A"
        received = packets_received.group(1) if packets_received else "N/A"
        lost = packets_lost.group(1) if packets_lost else "N/A"
        logging.info(f"{ip}: [PACKETS] Transmitted: {transmitted}, Received: {received}, Lost: {lost}%")

