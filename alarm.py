#@author: Baron Daugherty
#alarm.py
#alarm script activates a photoresistor circuit wired to the Raspberry Pi.
#in the event the laser light to the circuit is cut, it activates the Pi's
#camera module, takes a series of pictures, and e-mails the pictures of the
#perpetrator to your account of choice.
#Great for roommates who like to play pranks :)

#imports
import RPi.GPIO as GPIO, time, os
import picamera
import mailer

#some constants
#cell and color sets are the GPIO pin numbers
DEBUG = 1
CELL_POWER = 22
CELL_READ = 18
GREEN = 4
RED = 17
PATH = "path to where your camera will store its pictures"
AUDIO = "path to where your audio is stored (see below)"

#basic setup
def __init__():
	#use broadcom pin numbers, set pins for output power
	#power on to photoresistor and green led (system armed!)
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(CELL_POWER, GPIO.OUT)
	GPIO.setup(GREEN, GPIO.OUT)
	GPIO.setup(RED, GPIO.OUT)
	GPIO.output(CELL_POWER, GPIO.HIGH)
	GPIO.output(GREEN, GPIO.HIGH)

#take five pictures then wait five minutes
def takeFive():
	#counter, list of file names, date stamp
	#turn off green LED, turn on red LED
	#activate camera
	i = 0
	pics =[]
	date = time.strftime("%d-%m-%y")
	GPIO.output(GREEN, GPIO.LOW)
	GPIO.output(RED, GPIO.HIGH)
	camera = picamera.PiCamera()
	while i < 5:
		#when we reach the third picture, play an audio clip!
		#mine is a voice that says "What are you doing in here!?"
		#the idea is the perpetrator will turn around and look right at the camera
		if i == 3:
			os.system("aplay " +AUDIO +"WhatDoing.wav")
		#sleep 1 second, make a timestamp, snap a picture, add it to the list, increment counter
		time.sleep(1)
		timestamp = time.strftime("%X")
		camera.capture(PATH+date+"-"+timestamp+".jpg")
		pics.append(PATH+date+"-"+timestamp+".jpg")
		i+=1
	#mail our pictures then sleep five minutes (so this doesn't continually take pictures and bomb our inbox
	mailer.mail("from account", "password", "to account", "subject", "body text", pics)
	time.sleep(300)
	#switch LEDs back to green on / red off
	GPIO.output(RED, GPIO.LOW)
	GPIO.output(GREEN, GPIO.HIGH)

#this keeps a read on our resistor
def RCtime (RCpin):
	reading = 0
	#turn the input pin off and sleep .1 seconds
	GPIO.setup(RCpin, GPIO.OUT)
	GPIO.output(RCpin, GPIO.LOW)
	time.sleep(0.1)

	#switch input pin to IN
	GPIO.setup(RCpin, GPIO.IN)
	#increment reading for every low voltage cycle, return at high voltage
	while(GPIO.input(RCpin) == GPIO.LOW):
		reading += 1
	return reading
		
#run the thing
def main():
	#setup
	__init__()
	#infinite loop
	while True:
		#measure resistance
		resistance = RCtime(CELL_READ)
		#if resistance is above this threshold (test yours to find the best setting for the room you're in),
		#then take pictures
		if resistance > 200:
			takeFive()

main()
