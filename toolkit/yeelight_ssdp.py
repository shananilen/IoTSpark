import socket
import re
import argparse

MCAST_GRP = '239.255.255.250'
SRC_PORT = 4444

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)


def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py yeelight_ssdp",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This Module help to Discover yeelight ip's in the network",
                                     epilog="""Example usage:

    frame.py yeelight_ssdp -p 1982""")

    parser.add_argument("-p", "--port", help="Destination Port for yeelight", type=int)

    args = parser.parse_args(args)
    return args

def request(args):
	sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
	sock.bind(('', SRC_PORT))
	sock.sendto("M-SEARCH * HTTP/1.1\r\n\
	HOST: 239.255.255.250:1982\r\n\
	MAN: \"ssdp:discover\"\r\n\
	ST: wifi_bulb\r\n".encode(), (MCAST_GRP, args.port))

	# close this multicast socket
	sock.close()

	#and open a new receive socket on the same port
	sock_recv = socket.socket(
		socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
	sock_recv.bind(('', SRC_PORT))

	while True:
		data = sock_recv.recv(1024)
		print("done")
		results(data)


def results(data):
	filter_location = re.compile(
		"Location: {}_{}://[ ]*(.+)\r\n".format("protocol", "networkid"), re.IGNORECASE)
	print('found data: %s', data.decode())
	location_result = filter_location.search(data.decode())

	if location_result:
		peer_ip, peer_port = location_result.group(1).split(":")
		print('{}:{} is running the same protocal'.format(peer_ip, peer_port))

def module_main(args):
    args = parse_args(args)
    request(args)
    results()
