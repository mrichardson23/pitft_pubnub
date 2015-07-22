#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFont, ImageColor
import socket
import os
import RPi.GPIO as GPIO
from time import sleep
from pubnub import Pubnub
import credentials

buttonA = 17
buttonB = 22
buttonC = 23
buttonD = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Medium.ttf', 30)

def display(message):
	canvas = Image.new('RGBA', (240,320), (255,255,255,0))
	d = ImageDraw.Draw(canvas)

	#black background:
	d.rectangle([0,0,240,320], fill=(0,0,0))
	d.text((10,5), message, font=fnt, fill=(255,255,255))

	canvas = canvas.rotate(90)
	canvas.save("/tmp/test.png")
	os.system('sudo fbi -T 2 -d /dev/fb1 -noverbose /tmp/test.png')

pubnub = Pubnub(publish_key=credentials.PUBLISH_KEY, subscribe_key=credentials.SUBSCRIBE_KEY)

def callback(message, channel):
	display(message['text'])
  
def error(message):
	display("ERROR : " + str(message))
  
def connect(message):
	display("Conencted.")
  
def reconnect(message):
	print("RECONNECTED")
  
  
def disconnect(message):
	print("DISCONNECTED")

canvas = Image.new('RGBA', (240,320), (255,255,255,0))
d = ImageDraw.Draw(canvas)

#black background:
d.rectangle([0,0,240,320], fill=(0,0,0))
d.text((10,5), "Connecting...", font=fnt, fill=(255,255,255))

canvas = canvas.rotate(90)
canvas.save("/tmp/test.png")
os.system('sudo fbi -T 2 -d /dev/fb1 -noverbose /tmp/test.png')
  
pubnub.subscribe(channels='display', callback=callback, error=callback, connect=connect, reconnect=reconnect, disconnect=disconnect)

while True:
	pass

