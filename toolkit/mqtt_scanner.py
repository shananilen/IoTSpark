import socket
import sys
import argparse

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py mqtt_scanner",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This Module help to identy the MQTT Server",
                                     epilog="""Example usage:

    frame.py mqtt_scanner -ipran 192.168.8.""")
    parser.add_argument("-ipran", "--ip_addres_range",
                        help="Input IP address range (Ex 192.168.8.)", type=str)

    args = parser.parse_args(args)
    return args

def iprange(args):
    try:
        if args.ip_addres_range:
            for ip in range(100,220):
                addr = args.ip_addres_range + str(ip)
                sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = sock.connect_ex((addr,1883))
                if result == 0 :
                    print(addr, "This is a mqtt server")
                else:
                    sock.close()

    except socket.error:
        print("Couldn't connect ip range")
        sys.exit()

    except KeyboardInterrupt:
        sys.exit()

def module_main(args):
    args = parse_args(args)
    iprange(args)
