import random
import string
import sys
import argparse
from core.ip import DEFAULT_IP
import paho.mqtt.client as mqtt

ip_add = DEFAULT_IP

name = ''.join((random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(16)))

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py mqtt_topic_sniffer",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module is useful for sniffing the MQTT server topic",
                                     epilog="""Example usage:

    frame.py -ip 192.168.8.200 mqtt_topic_sniffer """)

    args = parser.parse_args(args)
    return args

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    er = client.subscribe('#', qos=1)
    er+= client.subscribe('$SYS/#')

    if er[0] == 0:
        print("Successfully subscribed to all system topics")
    else:
        print("Failed to subscribe to all system topics.")

def on_message(client, userdata, message):
    #print('Topic: %s | QOS: %s  | Message: %s' % (message.topic, message.qos, message.payload))
    with open("logdata/topic_details.txt", 'a') as outfile:
        outfile.write("Topic:{} | QOS:{} | Message:{}\n".format(message.topic,message.qos, message.payload))
    test_list = [message.topic]
    start_word = '$SYS'
    with_sys = [x for x in test_list if x.startswith(start_word)]
    without_sys = [x for x in test_list if x not in with_sys]
    without_sys_str = str(*without_sys)
    if with_sys!= test_list:
        print('Topic: %s | QOS: %s  | Message: %s' % (without_sys_str, message.qos, message.payload))

def top_sniffer():
    client = mqtt.Client(name)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(ip_add, 1883, 60)
    client.loop_forever()

def module_main(args):
    args = parse_args(args)
    top_sniffer()
