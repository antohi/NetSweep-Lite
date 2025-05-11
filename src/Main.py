from NetworkInfo import NetworkInfo
from PingTool import PingTool
from PortScanner import PortScanner
from RiskScanner import RiskScanner
from InputValidation import InputValidation
import logging
from datetime import datetime

# Initialize tools
ni = NetworkInfo()
pt = PingTool()
ps = PortScanner()
rs = RiskScanner()

logging.basicConfig(filename="net_log.txt", level=logging.INFO)
logging.info(datetime.now())

def ping_menu():
    # [IP PING TOOL]
    print("\n[IP PING TOOL]"
          "\n1) Ping Single/Multiple IPs"
          "\n2) Ping Range of IPs")
    return input("> ").strip()

def run_ping_tool():
    choice = ping_menu()
    # Choice 1 of Ping Tool
    if choice == "1":
        add_more = True
        print("\n--SINGLE/MULTIPLE IP PING TOOL--"
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
                print("\n[INVALID IP] Invalid IP address! Please enter a valid IP.\n")
            else:
                pt.add_ip(ip)

    # Choice 2 of Ping Tool
    elif choice == "2":
        print("\n--RANGE PING TOOL--")
        start = input("> ").strip()
        while not InputValidation.validate_ip(start):
            start = input("[INVALID IP] Enter START IP again: ").strip()
        end = input("END IP: ").strip()
        while not InputValidation.validate_ip(end):
            end = input("[INVALID IP] Enter END IP again: ").strip()
        print("\nPinging IP range...\n")
        pt.ping_addresses_in_range(start, end)
    else:
        print("[ERROR] Invalid choice in Ping Tool.")

def port_menu():
    # [PORT SCANNER]
    print("\n[PORT SCANNER]"
          "\n1) Scan Single Port"
          "\n2) Quick Scan (Top 10 Ports)"
          "\n3) Deep Scan (Top 25 Ports)")
    return input("> ").strip()

def run_port_scanner():
    choice = port_menu()
    if choice == "1":
        ip = input("IP address: ").strip()
        while not InputValidation.validate_ip(ip):
            ip = input("[INVALID IP] Enter a valid IP: ").strip()
        port = input("Port number: ").strip()
        print(f"\nScanning port {port} on {ip}...")
        ps.scan_single_port(port, ip)
    elif choice == "2":
        ip = input("IP address: ").strip()
        while not InputValidation.validate_ip(ip):
            ip = input("[INVALID IP] Enter a valid IP: ").strip()
        ps.quick_scan(ip)
    elif choice == "3":
        ip = input("IP address: ").strip()
        while not InputValidation.validate_ip(ip):
            ip = input("[INVALID IP] Enter a valid IP: ").strip()
        ps.deep_scan(ip)
    else:
        print("[ERROR] Invalid choice in Port Scanner.")

def log_system_info():
    # --SYS/NET INFO LOGGING--
    print("\n--SYS/NET INFO LOGGING--")
    print("Logging system & network information...")
    info = f"{ni.get_socket()} {ni.get_default_gateway()} {ni.get_dns_nameservers()}"
    ni.get_sys_info()
    print(info)

def run_service_risk_scan():
    # --SERVICE RISK SCAN--
    print("\n--SERVICE RISK SCAN--")
    ip = input("\nIP address: ").strip()
    while not InputValidation.validate_ip(ip):
        ip = input("[INVALID IP] Enter a valid IP: ").strip()
    print("\nDetecting risk in services (this may take a few minutes)...")
    rs.scan_banners(ip)

def main_menu():
    print("\n==========================="
          "\n[Welcome to NetworkChecker]"
          "\n===========================")
    print("\n[MENU]"
          "\n1) Diagnostics (Ping / Port Scanner)"
          "\n2) System / Network Info"
          "\n3) Service Risk Scan"
          "\n4) Quit")
    return input("> ").strip()

def main_loop():
    exit = False
    while not exit:
        choice = main_menu()
        if choice == "1":
            # Diagnostics submenu
            sub = input("\nDiagnostics:\n1) Ping Tool\n2) Port Scanner\n> ").strip()
            if sub == "1":
                run_ping_tool()
            elif sub == "2":
                run_port_scanner()
            else:
                print("[ERROR] Invalid Diagnostics choice.")
        elif choice == "2":
            log_system_info()
        elif choice == "3":
            run_service_risk_scan()
        elif choice == "4":
            exit = True
            print("\nThank you for using NetworkChecker. Have a great day!")
        else:
            print("[ERROR] Invalid menu choice.")
        if not exit:
            cont = input("\nReturn to Menu? (Y/N): ").strip().lower()
            if cont != "y":
                exit = True
                print("\nGoodbye!")

if __name__ == "__main__":
    main_loop()
