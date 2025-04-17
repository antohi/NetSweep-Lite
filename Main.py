from NetworkInfo import NetworkInfo
from PingTool import PingTool
import logging
from datetime import datetime
from PortScanner import PortScanner

logging.basicConfig(filename="net_log.txt", level=logging.INFO)

ni = NetworkInfo()
pt = PingTool()
ps = PortScanner()
inp = None
start_range = None
end_range = None

print("Welcome to NetworkChecker!")
# ssk if the user wants to log network info
logging.info(datetime.now())
print("\nWould you like to log your Network/System Info? (Y/N)")
inp = input().lower().strip()

if inp in ["y", "yes"]:
    net_info = f"{datetime.now()}:  {ni.get_socket()} {ni.get_default_gateway()} {ni.get_dns_nameservers()}"
    ni.get_sys_info()
    print(net_info)
elif inp in ["n", "no"]:
    print("Skipping logging of Network Info...")
else:
    print("Invalid input. Please enter 'Y' or 'N'")

exit = False
while not exit:
    print("\nPlease enter the number of the feature you'd like to access:"
          "\n1) IP Ping Tool"
          "\n2) Port Scanner")
    choice = input().lower().strip()
    if choice == "1":
        # loop for pinging IP addresses
        add_more = True
        while add_more:
            print("\nInput IPs to ping (one per line), if done press ENTER. To ping IPs in a range, type \"R\"")
            ip_to_ping = input()
            if ip_to_ping == "":
                add_more = False  # End the loop
            elif ip_to_ping.lower().strip() == "r":
                print("Please enter the starting IP of your range: ", end="")
                start_range = input()
                print("Please enter the ending IP of your range: ", end="")
                end_range = input()
                pt.ping_addresses_in_range(start_range, end_range)
                continue
            else:
                pt.add_ip(ip_to_ping)  # Add IP

        # Check for more IPs
        if not pt.get_addresses():
            print("No IP addresses were entered to ping.")
        else:
            print("Pinging IP addresses...")
            pt.ping_addresses()

    elif choice == "2":
        # Scan specific ports for an IP address
        print("\n[PORT SCANNER]"
              "\nPlease enter the number of the feature you'd like to access:"
              "\n1) Scan Single Port"
              "\n2) Quick Scan (Top 10 Ports)"
              "\n3) Deep Scan (Top 25 Ports)")
        choice = input()
        if choice == "1":
            print("\nInput the port: ")
            port = input()
            print("\nInput the IP address: ")
            ip = input()
            print("Scanning port...")
            ps.scan_single_port(port, ip)
        elif choice == "2":
            print("\nInput the IP address: ")
            ip = input()
            print("Scanning ports...")
            ps.quick_scan(ip)
        elif choice == "3":
            print("\nInput the IP address: ")
            ip = input()
            print("Scanning ports...")
            ps.deep_scan(ip)
    print("\nWould you like to continue? (Y/N)")
    inp = input().lower().strip()
    if inp == "y":
        continue
    else:
        exit = True
        print("\nProgram exited.")