# auto-Pi-bot
self navigating pi robot

The code is ran in python3 on raspbian buster 

requires pigpio library installed and the daemon running: http://abyz.me.uk/rpi/pigpio/download.html  
the adafruit motorkit library is also required: https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software
follow the instructions here to install dependancies for the waveshare e-ink display: https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT  


Dependent scripts:     

sonar_trigger_echo.py from the pigpio library  
epd2in13.py and epdconfig.py from waveshare's library 
(these are included in this repo)  

Hardware:  
Raspberry Pi Zero W  
Adafruit DC motor bonnet  
Waveshare V2 2.13 in E-ink display  
(See waveshare wiki for wiring and other documentation: https://www.waveshare.com/wiki/Main_Page  
Ultrasonic sensor w/ 1k and 2k ohm resistors on the echo line  
1 micro servo (for sensor)  
4 dc motors + wheels  
portable phone charger  
2x 18650 style batteries (for dc motors, servo, and sensor)  
A 5v regulator to supplies power from the two 18650's to the servo and sensor, this is to avoid modifying the pi to get the 5v output while the bonnet is attached the GPIO. The bonnet does not have a breakout for the pi's 5v. However with stacking headers, you can use the 5v from the GPIO.  
The housing and mount for the sensor and the housing for the display are 3D printed, the stl files were downloaded from thingiverse:  

Sensor housing: https://www.thingiverse.com/thing:35398  
Servo mount: https://www.thingiverse.com/thing:4408418  
Display holder: https://www.thingiverse.com/thing:4490552

![picture](img/20200628_172526.jpg)
Format: ![Alt Text](url)  

![picture2](img/20200702_212620.jpg)
Format: ![Alt Text](url)
