import socket
import struct
import time
import argparse

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
msg = 0b01000000
val = 0
def_time = 2
coap_pac = struct.pack('BB',msg,val)
s.settimeout(3)

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py coap_scanner",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This Module helps to identify the CoAP Server",
                                     epilog="""Example usage:

    frame.py coap_scanner -ipran 192.168.8.""")
    parser.add_argument("-ipran", "--ip_addres_range",
                        help="Input IP address range (Ex 192.168.8.)", type=str)

    args = parser.parse_args(args)
    return args


def pack_mon(args):
    if args.ip_addres_range:
        for ip in range(100,122):
            addr = args.ip_addres_range + str(ip)
            s.connect((addr ,5683))
            s.sendto(coap_pac,(addr,5683))
            try:
                m=s.recvfrom(100)
                if m[0]!=None:
                    print("This is a coap server : %s | This is a reply : %s" % (addr,m[0]))

            except socket.timeout:
                print("cannot connect" ,addr)

def module_main(args):
    args = parse_args(args)
    pack_mon(args)

#pack_mon()
