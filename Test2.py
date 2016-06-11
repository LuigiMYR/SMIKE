#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
reed = 4
def savetime(channel):
    print("Funktioniert")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(reed, GPIO.IN, GPIO.PUD_DOWN)

GPIO.add_event_detect(reed, GPIO.RISING, callback=savetime)
while True:
    time.sleep(1)
    
