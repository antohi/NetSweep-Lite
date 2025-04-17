from NetworkInfo import NetworkInfo
from PingTool import PingTool
import logging
from datetime import datetime
from PortScanner import PortScanner
from InputValidation import InputValidation
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
    print("\n[MENU]"
          "\nPlease enter the number of the feature you'd like to access:"
          "\n1) IP Ping Tool"
          "\n2) Port Scanner")
    choice = input().lower().strip()
    if choice == "1":
        # loop for pinging IP addresses
        print("\n[IP PING TOOL]"
              "\nPlease enter the number of the feature you'd like to access:"
              "\n1) Ping Single/Multiple IPs"
              "\n2) Ping Range of IPs")
        choice = input().lower().strip()
        if choice == "1":
            add_more = True
            print("\nInput IPs to ping (one per line)."
                  "\nIf finished, input \"x\".")
            while add_more:
                print(f"IP (\"x\" to END): ", end="")
                ip_to_ping = input()
                if ip_to_ping.lower().strip() == "x":
                    add_more = False  # End the loop
                    # Check if no IPs inputted
                    if not pt.get_addresses():
                        print("No IP addresses were entered to ping.")
                    else:
                        print("\nPinging IP addresses...\n")
                        pt.ping_addresses()
                if InputValidation.validate_ip(ip_to_ping) is False:
                    print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                else:
                    pt.add_ip(ip_to_ping)  # Add IP
            """
            if ip_to_ping.lower().strip() == "r":
                print("Please enter the starting IP of your range: ", end="")
                start_range = input()
                print("Please enter the ending IP of your range: ", end="")
                end_range = input()
                pt.ping_addresses_in_range(start_range, end_range)
                continue
            """

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