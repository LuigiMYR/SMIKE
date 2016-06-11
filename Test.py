#!/usr/bin/env python
#coding: utf8

import time
import RPi.GPIO as GPIO
reed = 4
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(reed, GPIO.IN, GPIO.PUD_DOWN)

while True:
    if GPIO.input(reed):
        print("Funktioniert")

    else:
        print("Funst nicht")
