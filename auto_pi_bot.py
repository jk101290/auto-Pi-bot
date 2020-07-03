import sys
sys.path.insert(1, "./lib")
import time
import sonar_trigger_echo
import pigpio
from adafruit_motorkit import MotorKit
import epd2in13_V2
from PIL import Image,ImageDraw,ImageFont

epd = epd2in13_V2.EPD()
font15 = ImageFont.truetype('Font.ttc', 15)
font24 = ImageFont.truetype('Font.ttc', 24)

pi = pigpio.pi()
kit = MotorKit()
sonar = sonar_trigger_echo.ranger(pi, 21, 20)

speed = 0.4
turnspeed = 0.5
min = 60
pwm_pin = 18
eyesfwd = 1500
eyesright = 500
eyesleft = 2500
sleep_time = 2

display_strings = ["Calculating distance...", " cm", "onward!!", "too close!!", "looking around... ", "looking right", "looking left", "ok, i'll go left", "ok, i'll go right", "invalid distance X_X", "trying again...", "bye!"]

def start_screen():
	epd.init(epd.FULL_UPDATE)
	epd.Clear(0xFF)
	image = Image.new('1', (epd.height, epd.width), 255)
	draw = ImageDraw.Draw(image)
	epd.init(epd.FULL_UPDATE)
	epd.displayPartBaseImage(epd.getbuffer(image))
	epd.init(epd.PART_UPDATE)
	draw.text((10, 50), "Hi! I'm ready to go!", font = font24, fill = 0)
	epd.displayPartial(epd.getbuffer(image))
	
def display_text(display_strings, i, dist):
	image = Image.new('1', (epd.height, epd.width), 255)
	draw = ImageDraw.Draw(image)
	draw.rectangle((40, 50, 220, 105), fill = 255)
	if dist == 0:
		draw.text((10, 50), display_strings[i], font = font24, fill = 0)
	elif dist > 0:
		draw.text((10, 50), str(dist), font = font24, fill = 0)
		draw.text((50, 50), display_strings[1], font = font24, fill = 0)
	epd.displayPartial(epd.getbuffer(image))

def forward():
	kit.motor1.throttle = -(speed)
	kit.motor2.throttle = -(speed)
	kit.motor3.throttle = speed
	kit.motor4.throttle = speed
		
def stop():
	kit.motor1.throttle = 0
	kit.motor2.throttle = 0
	kit.motor3.throttle = 0
	kit.motor4.throttle = 0
	
def turnLeft():
	print("turning left")
	pulse_width = pi.get_servo_pulsewidth(pwm_pin)
	if pulse_width != eyesleft:
		pi.set_servo_pulsewidth(pwm_pin, eyesleft)
	kit.motor1.throttle = turnspeed
	kit.motor2.throttle = turnspeed
	kit.motor3.throttle = turnspeed
	kit.motor4.throttle = turnspeed
	time.sleep(1)
	stop()
	time.sleep(1)
	main()

def turnRight():
	print("turning right")
	pulse_width = pi.get_servo_pulsewidth(pwm_pin)
	if pulse_width != eyesright:
		pi.set_servo_pulsewidth(pwm_pin, eyesright) 
	kit.motor1.throttle = -(turnspeed)
	kit.motor2.throttle = -(turnspeed)
	kit.motor3.throttle = -(turnspeed)
	kit.motor4.throttle = -(turnspeed)
	time.sleep(1)
	stop()
	time.sleep(1)
	main()

def calcavedistance():
	readings = [0, 0, 0, 0, 0]
	num = 0
	while num < 5:
		triptime = sonar.read()
		readings[num] = (triptime / 1000000.0) * 34030
		print(readings[num])
		num += 1
		time.sleep(0.03)
	cm = sum(readings) / len(readings)
	average = round(cm)	
	return average

def look():
	display_text(display_strings,5,0)
	print("looking right")
	pi.set_servo_pulsewidth(pwm_pin, eyesright)
	time.sleep(sleep_time)
	print("checking average distance to the nearest object to my right...")
	time.sleep(sleep_time)
	ave_right = calcavedistance()
	display_text(display_strings,1,ave_right)
	print("The average distance reading to the right is " + str(ave_right) + " cm")
	while ave_right < 1 or ave_right > 500:
		display_text(display_strings,9,0)
		time.sleep(1)
		display_text(display_strings,10,0)
		print("invalid reading... trying again")
		time.sleep(sleep_time)
		ave_right = calcavedistance()
		display_text(display_strings,1,ave_right)
		print("The average distance reading to the right is " + str(ave_right) + " cm")
	time.sleep(sleep_time)
	
	display_text(display_strings,6,0)
	print("looking left")
	pi.set_servo_pulsewidth(pwm_pin, eyesleft)
	time.sleep(sleep_time)
	print("checking average distance to the nearest object to my left...")
	ave_left = calcavedistance()
	display_text(display_strings,1,ave_left)
	print("The average distance reading to the left is " + str(ave_left) + " cm")
	time.sleep(sleep_time)
	while ave_left < 1 or ave_left > 500:
		display_text(display_strings,9,0)
		time.sleep(1)
		display_text(display_strings,10,0)
		print("invalid reading... trying again")
		time.sleep(sleep_time)
		ave_left = calcavedistance()
		display_text(display_strings,1,ave_left)
		print("The average distance reading to the left is " + str(ave_left) + " cm")
	
	if ave_left > ave_right:
		display_text(display_strings,7,0)
		print("ok, I'll go left")
		time.sleep(sleep_time)
		turnLeft()
	elif ave_right > ave_left:
		display_text(display_strings,8,0)
		print("ok, I'll go right")
		time.sleep(sleep_time)
		turnRight()

def main(): 
	print("looking forward, if I'm not already")
	time.sleep(1)
	pulse_width = pi.get_servo_pulsewidth(pwm_pin)
	if pulse_width != eyesfwd:
		pi.set_servo_pulsewidth(pwm_pin, eyesfwd)
	
	display_text(display_strings,0,0)
	print("Checking average distance readings...")
	ave = calcavedistance()
	display_text(display_strings,1,ave)
	print("The average distance reading is " + str(ave) + " cm")
	time.sleep(1)
	
	count = 0
	
	while ave > min:
		if count == 0:
			display_text(display_strings,2,0)
			print("onward!")
		forward()
		print("Checking average distance readings...")
		ave = calcavedistance()
		print("The average distance reading is " + str(ave) + " cm")
		count += 1
		time.sleep(0.05)
	
	if ave <= min:
	   display_text(display_strings,3,0)
	   print("too close")
	   stop()
	   time.sleep(1)
	   display_text(display_strings,4,0)
	   print("looking around...")
	   look()
		
try:
	start_screen()
	pi.set_servo_pulsewidth(pwm_pin, eyesfwd)
	print("wait for 2s...")
	time.sleep(sleep_time)
	main()
except(KeyboardInterrupt):
	display_text(display_strings,11,0)
	stop()
	sonar.cancel()
	pi.stop()
	epd2in13_V2.epdconfig.module_exit()
