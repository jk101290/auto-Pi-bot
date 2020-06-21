import pigpio
import sonar_trigger_echo
import time
from adafruit_motorkit import MotorKit

kit = MotorKit()

pi = pigpio.pi()

sonar = sonar_trigger_echo.ranger(pi, 21, 20)

speed = 0.3
turnspeed = 0.5

max = 100

pin = 18 
duty = 1500 

wait = 0.2
wait2 = 1


def look():
    print("looking right")
    pi.set_servo_pulsewidth(pin, 500)
    time.sleep(wait2)
    print("checking how far away the nearest object to my right is...")
    time.sleep(wait2)
    cmRight = sonar.read() / 1000000.0 * 34030
    print("the nearest object to my right is " + str(cmRight) + " cm")
    time.sleep(wait2)
    print("looking left")
    pi.set_servo_pulsewidth(pin, 2500)
    time.sleep(wait2)
    print("checking how far away the nearest object to my left is...")
    cmLeft = sonar.read() / 1000000.0 * 34030
    time.sleep(wait2)
    print("the nearest object to my left is " + str(cmLeft) + " cm")
    time.sleep(wait2)
    if cmLeft > cmRight:
        print("ok, I'll go left")
        time.sleep(wait2)
        turnLeft()
    elif cmRight > cmLeft:
        print("ok, I'll go right")
        time.sleep(wait2)
        turnRight()

def turnLeft():
    print("turning left")
    pulse_width = pi.get_servo_pulsewidth(pin)
    if pulse_width != 2500:
        pi.set_servo_pulsewidth(pin, 2500)	
    time.sleep(wait2)
    kit.motor1.throttle = turnspeed
    kit.motor2.throttle = turnspeed
    kit.motor3.throttle = turnspeed
    kit.motor4.throttle = turnspeed
    time.sleep(wait2)
    stop()

def turnRight():
    print("turning right")
    pulse_width = pi.get_servo_pulsewidth(pin)
    if pulse_width != 500:
        pi.set_servo_pulsewidth(pin, 500)	
    time.sleep(wait2)
    kit.motor1.throttle = -(turnspeed)
    kit.motor2.throttle = -(turnspeed)
    kit.motor3.throttle = -(turnspeed)
    kit.motor4.throttle = -(turnspeed)
    time.sleep(wait2)
    stop()

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

pi.set_servo_pulsewidth(pin, duty)

while True:
    print("looking forward, if I'm not already")
    time.sleep(wait)
    pulse_width = pi.get_servo_pulsewidth(pin)
    if pulse_width != 1500:
        pi.set_servo_pulsewidth(pin, duty)
		
    print("checking how far away the nearest object is...")
    time.sleep(wait)	
    cm = sonar.read() / 1000000.0 * 34030
    print("the nearest object is " + str(cm) + " cm")
    time.sleep(wait)

    if cm > max:
        print("onward!")
        forward()
    else:
        print("too close, I'm gonna look around...")
        stop()
        time.sleep(wait2)
        look()
