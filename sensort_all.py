# -*- coding: utf-8 -*-
#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

sensor = 23

print ("모션 감지센서 준비중")
time.sleep(2)
while True:
		GPIO.setup(sensor, GPIO.IN)
		if GPIO.input(sensor):
			time.sleep(2)
			import sucOrfail
			
			break
			
	

	
	


