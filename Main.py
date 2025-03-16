import subprocess

from NetworkUptime import NetworkUptime

addresses = []
"""
print("Input IP/s: (ENTER to finish) ")
while True:
    address = input()
    if address == "":
        print("Pinging ... \n")
        break
    addresses.append(address)
"""
check = NetworkUptime(addresses)
check.get_default_gateway()



