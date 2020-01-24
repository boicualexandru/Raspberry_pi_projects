from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)

def blink_stop(onTime, offTime):
    GPIO.output(8, GPIO.HIGH)
    sleep(onTime)
    
    GPIO.output(8, GPIO.LOW)
    sleep(offTime)
    

while True:
    blink_stop(1,1)
    
    