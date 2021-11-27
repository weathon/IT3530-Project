from RPi import GPIO
import time

GPIO.setmode(GPIO.BCM) # [13] 
GPIO.setup(20, GPIO.OUT)

for i in range(100, 500, 10):
 GPIO.setup(20, GPIO.OUT)
 print(i)
 pin = GPIO.PWM(20, i)
 pin.start(10) # Duty cycle [14]
 time.sleep(1)
 pin.stop()
 time.sleep(0.5)
 
