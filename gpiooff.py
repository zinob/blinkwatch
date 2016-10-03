#!/usr/bin/python3

import RPi.GPIO as GPIO

def set_off(chanel):
	GPIO.setup(chanel, GPIO.OUT)
	GPIO.output(chanel, False)
	
GPIO.setmode(GPIO.BCM)
set_off(2)
set_off(3)
set_off(4)
