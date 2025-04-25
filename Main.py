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

print("\n==========================="
      "\n[Welcome to NetworkChecker]"
      "\n===========================")

# Logs date and time when program starts
logging.info(datetime.now())
exit = False

# Loop until program exits
while not exit:
    # Main menu
    print("\n[MENU]"
          "\nPlease enter the number of the feature you'd like to access:"
          "\n1) IP Ping Tool"
          "\n2) Port Scanner"
          "\n3) Log System/Network Information"
          "\n>", end=" ")
    choice = input().lower().strip()

    # Main Menu choice 1 - IP Ping Tool
    if choice == "1":
        print("\n[IP PING TOOL]"
              "\nPlease enter the number of the feature you'd like to access:"
              "\n1) Ping Single/Multiple IPs"
              "\n2) Ping Range of IPs")
        choice = input().lower().strip()
        # Choice 1 of Ping Tool
        if choice.strip() == "1":
            add_more = True
            print("\n--SINGLE/MULTIPLE IP PING TOOL--"
                  "\nInput IPs to ping (one per line)."
                  "\nIf finished, input \"x\".\n")

            # User can keep entering addresses until "x" is entered, sets add_more to False
            while add_more:
                print(f"IP (\"x\" to END): ", end="")
                ip_to_ping = input()

                if ip_to_ping.lower().strip() == "x":
                    add_more = False  # End the loop, user entered "x"
                    if not pt.get_addresses(): # Check if no addresses were entered
                        print("\nNo IP addresses were entered to ping.")
                    else:
                        print("\nPinging IP addresses...\n")
                        pt.ping_addresses(pt.get_addresses()) # Ping IP addresses entered

                # Check if IP entered is a valid IP address
                elif InputValidation.validate_ip(ip_to_ping) is False:
                    print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                else:
                    pt.add_ip(ip_to_ping)  # Adds IP if valid

        # Choice 2 of Ping Tool
        if choice.strip() == "2":
            print("\n--RANGE PING TOOL--"
                  "\nPlease input the START of the IP range: ", end="")
            start_range = input()
            while InputValidation.validate_ip(start_range) is False: # Makes sure starting range IP is valid
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Please input the START of the IP range: ", end="")
                start_range = input()
            print("\nPlease enter the END of the IP range: ", end="")
            end_range = input()
            while InputValidation.validate_ip(end_range) is False: # Makes sure ending range IP is valid
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Please input the END of the IP range: ", end="")
                end_range = input()
            print("\nPinging IP range...\n")
            pt.ping_addresses_in_range(start_range, end_range)

    # Main Menu choice 2 - Port Scanner
    elif choice == "2":
        print("\n[PORT SCANNER]"
              "\nPlease enter the number of the feature you'd like to access:"
              "\n1) Scan Single Port"
              "\n2) Quick Scan (Top 10 Ports)"
              "\n3) Deep Scan (Top 25 Ports)"
              "\n4) Banner Scan")
        choice = input()

        # Single port scan, one port, one IP
        if choice == "1":
            print("\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False: # Keeps asking user for valid IP
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nInput the port: ", end="")
            port = input()
            print(f"\nScanning port {port} in IP {ip}...")
            ps.scan_single_port(port, ip) # Scans single port and IP

        # Quick Scan, top 10 ports in desired IP
        elif choice == "2":
            print("\n--QUICK SCAN--"
                  "\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False: # Validates IP
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nScanning ports...")
            ps.quick_scan(ip)

        # Deep scan, top 25 ports in desired IP
        elif choice == "3":
            print("\n--DEEP SCAN--"
                  "\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False: # IP validation
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nScanning ports...", end="")
            ps.deep_scan(ip)

        # Retrieves banner information
        elif choice == "4":
            print("\n--SERVICE DETECTION--"
                  "\nInput the IP address: ", end="")
            ip = input()
            while InputValidation.validate_ip(ip) is False: # IP validation
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP address.\n")
                print("Input the IP address: ", end="")
                ip = input()
            print("\nDetecting services (this may take a few minutes)...")
            ps.scan_banners(ip)

    # Main Menu choice 3 - Logs system/network information
    elif choice == "3":
        print("\n--SYS/NET INFO LOGGING--")
        print("\nLogging system & network information...")
        net_info = f"{ni.get_socket()} {ni.get_default_gateway()} {ni.get_dns_nameservers()}"
        ni.get_sys_info()
        print(net_info)

    # Choice to return to main menu after any option is completed
    print("\nReturn to Menu? (Y/N)"
          "\n>", end=" ")
    inp = input().lower().strip()
    if inp == "y":
        continue
    else:
        exit = True
        print("\nThank you for using NetworkChecker. Have a great day!")
