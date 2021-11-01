import paho.mqtt.client as mqtt
import time
import logging
import random
import string
import argparse
from core.ip import DEFAULT_IP

logging.basicConfig(level=logging.INFO)

name = ''.join((random.choice(string.ascii_uppercase
               + string.ascii_lowercase + string.digits) for i in range(16)))

port = 1883

broker = DEFAULT_IP

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py mqtt_msg_create",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module help in the creation of mqtt server retained messages.",
                                     epilog="""Example usage:

    frame.py -ip 192.168.8.200 mqtt_msg_create -top home/light -msg1 on -msg2 off""")

    parser.add_argument("-top", "--topic", help="Topic to Publish in MQTT server", type=str)
    parser.add_argument("-msg1", "--message1", help="Message1 to Publish", type=str)
    parser.add_argument("-msg2", "--message2", help="Message2 to Publish", type=str)


    args = parser.parse_args(args)
    return args

def on_log(client, userdata, level, buf):
    logging.info(buf)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        logging.info("connected successfully")

    else:
        logging.info("Bad Connection: return code="+str(rc))
        client.loop_stop()


def on_disconnect(client, userdata, rc):
    logging.info("Client disconnected now")


def on_publish(client, userdata, mid):
    logging.info("In on_pub callback mid=" + str(mid))


def on_subscribe(client, userdata, mid, granted_qos):
    logging.info("subscribed")


def on_message(client, userdata, message):
    topic = str(message.topic)
    msgr = str(message.payload.decode("utf-8"))
    logging.info('Topic: %s | Message: %s' % (topic, msgr))


def publishing(args):
    mqtt.Client.connected_flag = False
    client = mqtt.Client(name)
    client.on_log = on_log
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_start()

    while not client.connected_flag:
        logging.info("In wait Loop")
        time.sleep(1)

    time.sleep(3)
    logging.info("publishing")
    ret = client.publish(args.topic, args.message1, 2, True)
    logging.info("publish return="+str(ret))
    time.sleep(3)
    ret = client.publish(args.topic, args.message2, 2, True)
    logging.info("publish return="+str(ret))
    time.sleep(3)
    client.subscribe(args.topic, 2)
    time.sleep(10)
    client.loop_stop()
    client.disconnect()

def module_main(args):
    args = parse_args(args)
    publishing(args)
