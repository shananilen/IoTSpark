import paho.mqtt.client as mqtt
import time
import random
import string
import argparse
from core.ip import DEFAULT_IP
import logging
logging.basicConfig(level=logging.INFO)

broker = DEFAULT_IP
port = 1883

name = ''.join((random.choice(string.ascii_uppercase
               + string.ascii_lowercase + string.digits) for i in range(16)))

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py mqtt_msg_delete",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This module help in the delete the mqtt server retained messages.",
                                     epilog="""Example usage:

    frame.py -ip 192.168.8.200 mqtt_msg_delete -top home/light""")

    parser.add_argument("-top", "--topic", help="Topic to Publish in MQTT server", type=str)

    args = parser.parse_args(args)
    return args

def on_message(client, userdata, message):
    topic = str(message.topic)
    msgr = str(message.payload.decode("utf-8"))
    logging.info('Deleting Topic: %s | Message: %s' % (topic, msgr))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
        logging.info("connected successfully")

    else:
        logging.info("Bad Connection: return code="+str(rc))
        client.loop_stop()


def on_subscribe(client, userdata, mid, granted_qos):
    logging.info("subscribed")


def on_log(client, userdata, level, buf):
    logging.info(buf)


def on_publish(client, userdata, mid):
    logging.info("In on_pub callback mid=" + str(mid))
    client.suback_flag = True


def reset(client,args):
    ret = client.publish(args.topic, "", 0, True)
    logging.info(str(ret))


def on_disconnect(client, userdata, rc):
    logging.info("Client disconnected")

def msg_delete(args):
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
    client.subscribe(args.topic, 2)
    #reset(client)
    time.sleep(10)
    client.loop_stop()
    client.disconnect()

def module_main(args):
    args = parse_args(args)
    msg_delete(args)
    client = mqtt.Client(name)
    reset(client,args)
