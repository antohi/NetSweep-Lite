from NetworkInfo import NetworkInfo
import subprocess
import socket

ni = NetworkInfo()
print(ni.get_default_gateway())
print(ni.get_dns_nameservers())



