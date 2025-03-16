import subprocess

address = ""
addresses = []
while address != "X":
    address = input("Address (\"X\" to stop): ")
    if address == "X":
        break
    addresses.append(address)

for address in addresses:
    p = subprocess.run(['ping', '-c', '1', address])

    if p.returncode == 0:
        print(address + " is up")
    else:
        print (address + " is down")



