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

print("\n============================"
      "\n[Welcome to NetworkChecker!]"
      "\n============================")
logging.info(datetime.now())
exit = False
while not exit:
    print("\n[MENU]"
          "\nPlease enter the number of the feature you'd like to access:"
          "\n1) IP Ping Tool"
          "\n2) Port Scanner"
          "\n3) Log System Information")
    choice = input().lower().strip()
    if choice == "1":
        # loop for pinging IP addresses
        print("\n[IP PING TOOL]"
              "\nPlease enter the number of the feature you'd like to access:"
              "\n1) Ping Single/Multiple IPs"
              "\n2) Ping Range of IPs")
        choice = input().lower().strip()
        if choice.strip() == "1":
            add_more = True
            print("\n--SINGLE/MULTIPLE IP PING TOOL--"
                  "\nInput IPs to ping (one per line)."
                  "\nIf finished, input \"x\".\n")
            while add_more:
                print(f"IP (\"x\" to END): ", end="")
                ip_to_ping = input()
                if ip_to_ping.lower().strip() == "x":
                    add_more = False  # End the loop
                    # Check if no IPs inputted
                    if not pt.get_addresses():
                        print("\nNo IP addresses were entered to ping.")
                    else:
                        print("\nPinging IP addresses...\n")
                        pt.ping_addresses(pt.get_addresses())
                elif InputValidation.validate_ip(ip_to_ping) is False:
                    print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                else:
                    pt.add_ip(ip_to_ping)  # Add IP

        if choice.strip() == "2":
            print("\n--RANGE PING TOOL--"
                  "\nPlease input the START of the IP range: ", end="")
            start_range = input()
            print("\nPlease enter the END of the IP range: ", end="")
            end_range = input()
            print("\nPinging IP range...\n")
            pt.ping_addresses_in_range(start_range, end_range)
    elif choice == "2":
        # Scan specific ports for an IP address
        print("\n[PORT SCANNER]"
              "\nPlease enter the number of the feature you'd like to access:"
              "\n1) Scan Single Port"
              "\n2) Quick Scan (Top 10 Ports)"
              "\n3) Deep Scan (Top 25 Ports)")
        choice = input()
        if choice == "1":
            print("\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False:
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nInput the port: ", end="")
            port = input()
            print(f"\nScanning port {port} in IP {ip}...")
            ps.scan_single_port(port, ip)
        elif choice == "2":
            print("\n--QUICK SCAN--"
                  "\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False:
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nScanning ports...")
            ps.quick_scan(ip)
        elif choice == "3":
            print("\n--DEEP SCAN--"
                  "\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False:
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nScanning ports...", end="")
            ps.deep_scan(ip)
    elif choice == "3":
        print("\n--SYSTEM INFO LOGGING--")
        print("\nLogging system information...")
        net_info = f"{ni.get_socket()} {ni.get_default_gateway()} {ni.get_dns_nameservers()}"
        ni.get_sys_info()
        print(net_info)
    print("\nReturn to Menu? (Y/N)")
    inp = input().lower().strip()
    if inp == "y":
        continue
    else:
        exit = True
        print("\nThank you for using NetworkChecker. Have a great day!")