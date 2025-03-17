from NetworkInfo import NetworkInfo
from PingTool import PingTool
import logging
from datetime import datetime

logging.basicConfig(filename="net_log.txt", level=logging.INFO)

ni = NetworkInfo()
pt = PingTool()
inp = None

print("Welcome to NetworkChecker!")
print("\nWould you like to log your Network Info? (Y/N)")
inp = input().lower().strip()
if inp.lower() in ["y", "yes"]:
    net_info = f"{datetime.now()}:  Local IP: {ni.get_socket()}, Gateway: {ni.get_default_gateway()}, DNS: {ni.get_dns_nameservers()}"
    print(net_info)
    logging.info(net_info)

elif inp.lower() in ["n", "no"]:
    print("Skipping logging of Network Info...")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")
print("Input IPs to ping, if done ENTER")
while (inp != ""):
    inp = input()
    if inp == "":
        break
    pt.add_ip(inp)
if not pt.get_addresses():
    print("No IP addresses were entered to ping.")
else:
    print(pt.ping_addresses())







