import subprocess
address = ""
addresses = []
while address != "X":
    address = input("Address (\"X\" to stop): ")
    if address == "X":
        break
    addresses.append(address)

for address in addresses:
    subprocess.run(['ping', '-c', '1', address])


