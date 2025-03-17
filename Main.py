from NetworkInfo import NetworkInfo

ni = NetworkInfo()
ips_to_ping = []
inp = None

print("Welcome to NetworkChecker!")
print("Input IPs to ping, if done ENTER")
while (inp != ""):
    inp = input()
    if inp == "":
        break
    ips_to_ping.append(inp)
if not ips_to_ping:
    print("No IP addresses were entered to ping.")
else:
    ni.ping_global(ips_to_ping)

print("\n\nWould you like to get the Local IP Address? (Y/N)")
inp = input().lower().strip()
if inp.lower() in ["y", "yes"]:
    print(ni.get_socket())
elif inp.lower() in ["n", "no"]:
    print("Skipping Local IP Address request.")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")

print("\n\nWould you like to get the Default Gateway IP? (Y/N)")
if inp.lower() in ["y", "yes"]:
    print(ni.get_default_gateway())
elif inp.lower() in ["n", "no"]:
    print("Skipping Default Gateway IP Address request.")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")

print("\n\nWould you like to get the DNS Nameservers? (Y/N)")
inp = input()
if inp.lower() in ["y", "yes"]:
    print(ni.get_dns_nameservers())
elif inp.lower() in ["n", "no"]:
    print("Skipping DNS Nameserver request.")
else:
    print("Invalid input. Please enter 'Y' or 'N'.")



