import socket
from common_ports import ports_and_services

def is_ip(address):
	return not address.split('.')[-1].isalpha()

def get_open_ports(target, port_range, verbose):
	ip = None
	url = None

	if is_ip(target):
		try:
			socket.inet_aton(target)
			ip = target
		except:
			return 'Invalid IP Adress'
	else:
		try:
			ip = socket.gethostbyname(target)
			url = target
		except socket.error:
			return 'Invalid Hostname'
		
	if not url:
		try:
			url = socket.gethostbyaddr(ip)[0]
		except socket.error:
			url = None
	
	first = port_range[0]
	last = port_range[1]
	open_ports = []

	for port in range(first, last + 1):
		soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		soc.settimeout(5)
		if not soc.connect_ex((ip, port)):
			open_ports.append(port)
		soc.close()
	
	if verbose == True:
		header = "Open ports for {} ({})\nPORT\tSERVICE\n".format(url, verbose, target)
		for port in open_ports:
			srvc = ports_and_services[port]
			portstr = "{}\t{}\n".format(port, srvc)
			str = header + portstr
			return str
	else:
		return(open_ports)