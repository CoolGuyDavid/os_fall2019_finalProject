#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import math
import requests

#Hue Lights API URL
url = 'http://192.168.1.162/api/WE73Ff1yupf8e8B5FXzTGlEPPLSZj4HMx4HPRcGR/lights/1/state'
off = '{"on":false}'
on = '{"on":true}'

def lightOn():
	print "Turning on light"
	request = requests.put(url, on)
	print(request)
	print "Successful"

def lightOff():
	print "Turning off light"
	request = requests.put(url, off)
	print(request)
	print "Successful"
def setHue(hue):
	payload = '{"hue":' +str(hue)+ '}'
 	#print payload
	#return '{"hue":',hue,'}'
	request = requests.put(url, payload)
	print(request)
def convertDistance(distance):
	hue = distance*245
	hue = int(hue)
	print hue
	setHue(hue)
def setBrightness(bri):
	payload = '{"bri":' +str(bri)+ '}'
 	#print payload
	#return '{"bri":',bri,'}'
	request = requests.put(url, payload)
	print(request)
def distanceToBri(distance):
	bri = distance*0.95
	bri = int(bri)
	bright = 254 - bri
	print bri
	setBrightness(bright)



def getDistance():
	try:
		GPIO.setmode(GPIO.BOARD)

		PIN_TRIGGER = 7
		PIN_ECHO = 11
		GPIO.setup(PIN_TRIGGER, GPIO.OUT)
		GPIO.setup(PIN_ECHO, GPIO.IN)
		GPIO.output(PIN_TRIGGER, GPIO.LOW)
		
	#	print "Waiting for sensor to settle"
	#	time.sleep(2)
	#	print "Calculating distance"
		GPIO.output(PIN_TRIGGER, GPIO.HIGH)
		time.sleep(0.00001)
		GPIO.output(PIN_TRIGGER, GPIO.LOW)


		while GPIO.input(PIN_ECHO)== 0:
			pulse_start_time = time.time()
		while GPIO.input(PIN_ECHO) == 1:
			pulse_end_time = time.time()
		pulse_duration = pulse_end_time - pulse_start_time
		distance = round(pulse_duration * 17150, 2)
		#print "",distance,"cm"
		return math.floor(distance)

	finally:
		GPIO.cleanup()

def main():
	setHue(5045)
	lightOn()
	change = False
	count = 0
	while True:
		time.sleep(.75)
		distance = getDistance()
		if distance < 10 and change == False:
			lightOff()
			change = True
			count += 1
			print count
		elif distance > 10 and change == True:
			lightOn()
			change = False
			count += 1
			print count
		print distance
	#lightOn()
	#lightOff()	

	
def modeNightLight():
	lightOn()
	setHue(8500)
	while True:
		distance = getDistance()
		distanceToBri(distance)
		print distance
		time.sleep(2)



modeNightLight()
