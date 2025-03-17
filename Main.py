from NetworkInfo import NetworkInfo

ni = NetworkInfo()
ni.ping_global(["8.8.8.8"])
ni.get_socket()
ni.get_default_gateway()
ni.get_dns_nameservers()




