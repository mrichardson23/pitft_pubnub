#!/usr/bin/python
from PIL import Image, ImageDraw, ImageFont, ImageColor
import socket
import os
import RPi.GPIO as GPIO
from time import sleep
from pubnub import Pubnub
import credentials
import textwrap

buttonA = 17
buttonB = 22
buttonC = 23
buttonD = 27

w = 240
h = 321

GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonC, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
fnt = ImageFont.truetype('/usr/share/fonts/truetype/roboto/Roboto-Medium.ttf', 20)

def display(message, color=(255,255,255)):
	canvas = Image.new('RGBA', (w,h), (0,0,0))
	d = ImageDraw.Draw(canvas)

	lines = textwrap.wrap(message, width=22)
	y = 0
	for line in lines:
		d.text((10,y), line, font=fnt, fill=color)
		y = y+22

	canvas = canvas.rotate(90)
	canvas.save("/tmp/test.png")
	os.system('sudo fbi -T 2 -d /dev/fb1 -noverbose /tmp/test.png')

pubnub = Pubnub(publish_key=credentials.PUBLISH_KEY, subscribe_key=credentials.SUBSCRIBE_KEY)

def callback(message, channel):
	display(message['text'])
  
def error(message):
	display("ERROR : " + str(message), color=(255,0,0))
  
def connect(message):
	display("Conencted.", color=(0,255,0))
  
def reconnect(message):
	print("RECONNECTED")
  
  
def disconnect(message):
	print("DISCONNECTED")

canvas = Image.new('RGBA', (240,320), (255,255,255,0))
d = ImageDraw.Draw(canvas)

display("Connecting...", color=(255,128,0))
  
pubnub.subscribe(channels='display', callback=callback, error=callback, connect=connect, reconnect=reconnect, disconnect=disconnect)

while True:
	if(GPIO.input(buttonD) == False):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.connect(('8.8.8.8', 0))
			local_ip_address = s.getsockname()[0]
		except:
			local_ip_address = "No IP"
		display(local_ip_address)
		sleep(1)

