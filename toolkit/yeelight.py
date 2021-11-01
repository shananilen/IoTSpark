import asyncio
import logging
import pprint
import argparse
from core.ip import DEFAULT_IP

from yeelight.aio import AsyncBulb

BULBIP = "{""}".format(DEFAULT_IP)

logging.basicConfig(level=logging.DEBUG)

def parse_args(args):
    parser = argparse.ArgumentParser(prog="frame.py yeelight",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description="This Module control yeelight bulb the network",
                                     epilog="""Example usage:

    frame.py -ip 192.168.8.119 yeelight""")

    args = parser.parse_args(args)
    return args

def my_callback(data):
    pprint.pprint(data)

async def yeelight_asyncio_demo():
    bulb = AsyncBulb(BULBIP)
    await bulb.async_listen(my_callback)
    print("turn on:", await bulb.async_turn_on())
    await asyncio.sleep(2)
    print("turn off:", await bulb.async_turn_off())
    await asyncio.sleep(2)
    print("turn on:", await bulb.async_turn_on())
    for i in range(10):
        brightness = (i + 1) * 10
        print(
            f"set brightness {brightness}:", await bulb.async_set_brightness(brightness)
        )
        await asyncio.sleep(1)
    await asyncio.sleep(500)
    await bulb.async_stop_listening()

def module_main(args):
    args = parse_args(args)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(yeelight_asyncio_demo())
