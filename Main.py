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
print("\nWould you like to log your Network/System Info? (Y/N)")
inp = input().lower().strip()

if inp in ["y", "yes"]:
    net_info = f"{datetime.now()}:  {ni.get_socket()} {ni.get_default_gateway()} {ni.get_dns_nameservers()}"
    ni.get_sys_info()
    print(net_info)
elif inp in ["n", "no"]:
    print("Skipping logging of Network Info...")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")

# loop for pinging IP addresses
add_more = True
while add_more:
    print("\nInput IPs to ping, if done press ENTER (one per line). To ping IPs in a range, type \"R\"")

    inp = input()
    if inp == "":
        break  # End the loop
    elif inp.lower().strip() == "r":
        print("Please enter the starting IP of your range: ", end="")
        start_range = input()
        print("Please enter the ending IP of your range: ", end="")
        end_range = input()
        print("Pinging IP addresses...")
        pt.ping_addresses_in_range(start_range, end_range)
    else:
        pt.add_ip(inp)  # Add IP

# Check for more IPs
if not pt.get_addresses():
    print("No IP addresses were entered to ping.")
else:
    print("Pinging IP addresses...")
    print(pt.ping_addresses())

