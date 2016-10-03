#!/usr/bin/python3
import requests
import shelve
import time 
import blinkenq
import configparser
import os


def check_status(blinkqueue,working=0,warning=1,error=2,url="",keys=[],interval=60):
    b=blinkqueue
    try:
        b.blink(working,50,10)
        r=requests.get(url).json()
        b.blink(working,0,10)
        if False in ( r[i] for i,_ in keys):
            b.blink(error,100,interval-1)
        else: 
            b.blink(error,0,interval-1)
    except (KeyError, ValueError, requests.exceptions.ConnectionError):
        b.blink(warning,1,interval-1)

def welcome(b,working=0,warning=1,error=2):
    b.blink(working,50,1)
    time.sleep(.5)
    b.blink(warning,20,1)
    time.sleep(.5)
    b.blink(error,30,1)
    time.sleep(2)

def read_config(config_file_name):
    configset = {}

    config = configparser.ConfigParser(allow_no_value=True)
    config.read(config_file_name)

    configset.update({k:int(v) for k,v in config['LEDS'].items()})
    configset['url'] = config.get('TARGET','url')
    configset['interval'] = config.getint('TARGET','interval')
    configset['keys'] = config.items('KEYS')
    
    return configset

if __name__ == "__main__":
    config=read_config(os.path.join(os.path.dirname(os.path.realpath(__file__)),"watcher.ini"))

    b=blinkenq.Blinkenq()
    b.setDaemon(True)
    b.start()

    welcome(b)
    try: 
        while True:
            check_status(b,**config)
            time.sleep(config['interval'])

    finally:
        for i in range(3):
            b.blink(i,0,config['interval']+2)
