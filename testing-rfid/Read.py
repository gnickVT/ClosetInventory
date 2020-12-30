#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

reader = SimpleMFRC522()

try:
    print("Hold a tag near the reader")
    id, text = reader.read()
    #print(id)
    #print(text)
    print("ID: %s\nText: %s" % (id, text))
finally:
    GPIO.cleanup()

