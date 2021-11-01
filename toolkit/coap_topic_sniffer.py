import socket
import sys
import argparse
from core.ip import DEFAULT_IP
from coapthon.client.helperclient import HelperClient

host = DEFAULT_IP
port = 5683

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py coap_topic_sniffer",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module is useful for sniffing the coap server topic.",
                                     epilog="""Example usage:

    frame.py -ip 192.168.8.113 coap_topic_sniffer""")

    args = parser.parse_args(args)
    return args


def coap_topic():
    client = HelperClient(server=(host, port))
    response = client.discover()
    print(response.pretty_print())
    client.stop()

def module_main(args):
    args = parse_args(args)
    coap_topic()
