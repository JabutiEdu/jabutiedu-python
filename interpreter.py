#!/usr/bin/env python

import os
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.output(23, GPIO.LOW)
GPIO.output(24, GPIO.LOW)
GPIO.output(17, GPIO.LOW)
GPIO.output(22, GPIO.LOW)

def parar():
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(17, GPIO.LOW)
    GPIO.output(22, GPIO.LOW)
    GPIO.cleanup()

def desligar():
    GPIO.output(9, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.cleanup()

message = sys.argv[1]
time = int(sys.argv[2])
if message == 'pf':
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(23, GPIO.LOW)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    time.sleep(time)
    parar()
elif message == 'pt':
    GPIO.output(24, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(17, GPIO.LOW)
    time.sleep(time)
    parar()
elif message == 'pe':
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(22, GPIO.HIGH)
    GPIO.output(17, GPIO.LOW)
    time.sleep(time)
    parar()
elif message == 'lde':
    GPIO.output(9, GPIO.HIGH)
    GPIO.output(11, GPIO.HIGH)
    time.sleep(time)
    desligar()
elif message == 'ld':
    GPIO.output(9, GPIO.HIGH)
    time.sleep(time)
    desligar()
elif message == 'le':
    GPIO.output(11, GPIO.HIGH)
    time.sleep(time)
    desligar()
elif message == 'pd':
    GPIO.output(24, GPIO.LOW)
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(17, GPIO.HIGH)
    GPIO.output(22, GPIO.LOW)
    time.sleep(time)
    parar()
elif message == 'som':
    os.system("espeak \"oi, eu sou a jabuti edu\" -v portugal -s140 -p60 -g2 -a100")
elif message == 'musica':
    os.system("mpg321 /home/pi/musica.mp3")
