from NetworkInfo import NetworkInfo
from PingTool import PingTool
from PortScanner import PortScanner
from RiskScanner import RiskScanner
from InputValidation import InputValidation
import logging
from datetime import datetime
from colorama import Fore, Style, init


# NMap Scan Me: 45.33.32.156

# Initialize tools
ni = NetworkInfo()
pt = PingTool()
ps = PortScanner()
rs = RiskScanner()

logging.basicConfig(filename="net_log.txt", level=logging.INFO)
logging.info(datetime.now())

# Ping Tool Menu options
def ping_menu():
    # [IP PING TOOL]
    print(f"\n{Fore.GREEN}[IP PING TOOL]{Style.RESET_ALL}"
          "\n1) Ping Single/Multiple IPs"
          "\n2) Ping Range of IPs")
    return input("> ").strip()

# Runs different ping tools based on option selected
def run_ping_tool():
    choice = ping_menu()
    # Choice 1 of Ping Tool
    if choice == "1":
        add_more = True
        print(f"\n{Fore.GREEN}--SINGLE/MULTIPLE IP PING TOOL--{Style.RESET_ALL}"
              "\nInput IPs to ping (one per line)."
              "\nIf finished, input \"x\".\n")
        while add_more:
            ip = input("IP (\"x\" to END): ").strip()
            if ip.lower() == "x":
                add_more = False
                if not pt.get_addresses():
                    print("\nNo IP addresses were entered to ping.")
                else:
                    print("\nPinging IP addresses...\n")
                    pt.ping_addresses(pt.get_addresses())
            elif not InputValidation.validate_ip(ip):
                print(f"{Fore.RED}\n[INVALID IP] Invalid IP address! Please enter a valid IP.\n{Style.RESET_ALL}")
            else:
                pt.add_ip(ip)

    # Choice 2 of Ping Tool
    elif choice == "2":
        print(f"\n{Fore.GREEN}--RANGE PING TOOL--{Style.RESET_ALL}")
        start = input("START IP: ").strip()
        while not InputValidation.validate_ip(start):
            start = input(f"{Fore.RED}[INVALID IP] Enter START IP again: {Style.RESET_ALL}").strip()
        end = input("END IP: ").strip()
        while not InputValidation.validate_ip(end):
            end = input(f"{Fore.RED}[INVALID IP] Enter END IP again: {Style.RESET_ALL}").strip()
        print("\nPinging IP range...\n")
        pt.ping_addresses_in_range(start, end)
    else:
        print(f"{Fore.RED}[ERROR] Invalid choice in Ping Tool.{Style.RESET_ALL}")

# Port scan menu options
def port_menu():
    # [PORT SCANNER]
    print(f"\n{Fore.LIGHTCYAN_EX}[PORT SCANNER]{Style.RESET_ALL}"
          "\n1) Scan Single Port"
          "\n2) Quick Scan (Top 10 Ports)"
          "\n3) Deep Scan (Top 25 Ports)")
    return input("> ").strip()

# Runs different types of port scans based on option
def run_port_scanner():
    choice = port_menu()
    if choice == "1":
        print(f"\n{Fore.CYAN}--SINGLE PORT SCAN--{Style.RESET_ALL}")
        ip = input("IP address: ").strip()
        while not InputValidation.validate_ip(ip):
            ip = input(f"{Fore.RED}[INVALID IP] Enter a valid IP: {Style.RESET_ALL}").strip()
        port = input("Port number: ").strip()
        print(f"\nScanning port {port} on {ip}...")
        ps.scan_single_port(port, ip)
    elif choice == "2":
        print(f"\n{Fore.CYAN}--QUICK PORT SCAN--{Style.RESET_ALL}")
        ip = input("IP address: ").strip()
        while not InputValidation.validate_ip(ip):
            ip = input(f"{Fore.RED}[INVALID IP] Enter a valid IP: {Style.RESET_ALL}").strip()
        ps.quick_scan(ip)
    elif choice == "3":
        print(f"\n{Fore.CYAN}--DEEP PORT SCAN--{Style.RESET_ALL}")
        ip = input("IP address: ").strip()
        while not InputValidation.validate_ip(ip):
            ip = input(f"{Fore.RED}[INVALID IP] Enter a valid IP: {Style.RESET_ALL}").strip()
        ps.deep_scan(ip)
    else:
        print(f"{Fore.RED}[ERROR] Invalid choice in Port Scanner.{Style.RESET_ALL}")

# Logs system info at the time of usage
def log_system_info():
    # --SYS/NET INFO LOGGING--
    print(f"\n{Fore.WHITE}--SYS/NET INFO LOGGING--{Style.RESET_ALL}")
    print("Logging system & network information...")
    info = f"{ni.get_socket()} {ni.get_default_gateway()} {ni.get_dns_nameservers()}"
    ni.get_sys_info()
    print(info)

# Initiates services risk scan to find any CVEs
def run_service_risk_scan():
    # --SERVICE RISK SCAN--
    print(f"{Fore.MAGENTA}\n--SERVICE RISK SCAN--{Style.RESET_ALL}")
    ip = input("IP address: ").strip()
    while not InputValidation.validate_ip(ip):
        ip = input(f"{Fore.RED}[INVALID IP] Enter a valid IP: {Style.RESET_ALL}").strip()
    print("\nDetecting risk in services (this may take a few minutes)...")
    rs.scan_banners(ip)

# Main menu
def main_menu():
    print(f"\n{Fore.YELLOW}==========================="
          f"\n{Fore.LIGHTYELLOW_EX}     [NetSweep Lite]{Style.RESET_ALL}"
          f"\n{Fore.YELLOW}==========================={Style.RESET_ALL}")
    print(f"\n{Fore.LIGHTBLUE_EX}[MENU]{Style.RESET_ALL}"
          "\n1) Diagnostics (Ping / Port Scanner)"
          "\n2) System / Network Info"
          "\n3) Service Risk Scan"
          "\n4) Quit")
    return input("> ").strip()

# UI loop
def main_loop():
    exit = False
    while not exit:
        choice = main_menu()
        if choice == "1":
            # Diagnostics submenu
            sub = input(f"\n{Fore.BLUE}[DIAGNOSTICS]{Style.RESET_ALL}\n1) Ping Tool\n2) Port Scanner\n> ").strip()
            if sub == "1":
                run_ping_tool()
            elif sub == "2":
                run_port_scanner()
            else:
                print(f"{Fore.RED}[ERROR] Invalid Diagnostics choice.{Style.RESET_ALL}")
        elif choice == "2":
            log_system_info()
        elif choice == "3":
            run_service_risk_scan()
        elif choice == "4":
            exit = True
            print(f"{Fore.LIGHTYELLOW_EX}\nThank you for using NetworkChecker. Have a great day!{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[ERROR] Invalid menu choice.{Style.RESET_ALL}")
            continue
        if not exit:
            cont = input(f"{Fore.YELLOW}\nReturn to Menu? (Y/N): {Style.RESET_ALL}").strip().lower()
            if cont != "y":
                exit = True
                print(f"{Fore.BLUE}\nGoodbye!{Style.RESET_ALL}")

if __name__ == "__main__":
    main_loop()