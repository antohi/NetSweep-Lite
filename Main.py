from NetworkInfo import NetworkInfo
from PingTool import PingTool
import logging
from datetime import datetime

logging.basicConfig(filename="net_log.txt", level=logging.INFO)

ni = NetworkInfo()
pt = PingTool()
inp = None

print("Welcome to NetworkChecker!")

# ssk if the user wants to log network info
print("\nWould you like to log your Network Info? (Y/N)")
inp = input().lower().strip()

if inp in ["y", "yes"]:
    net_info = f"{datetime.now()}:  Local IP: {ni.get_socket()}, Gateway: {ni.get_default_gateway()}, DNS: {ni.get_dns_nameservers()}"
    print(net_info)
elif inp in ["n", "no"]:
    print("Skipping logging of Network Info...")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")

# loop for pinging IP addresses
add_more = True
while add_more:
    print("\nInput IPs to ping, if done ENTER (one per line)")

    inp = input()
    if inp == "":
        break
    else:
        pt.add_ip(inp)

    # check for more IPs
if not pt.get_addresses():
    print("No IP addresses were entered to ping.")
else:
    print("Pinging IP addresses...")
    print(pt.ping_addresses())

