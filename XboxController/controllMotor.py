#we will import the sleep module driver motorfrom the time library
from time import sleep

from evdev import InputDevice, categorize, ecodes
#cree un objet gamepad | creates object gamepad
gamepad = InputDevice('/dev/input/event0')
analogMax = 65535
analogMid = (analogMax + 1) / 2
analogKey = 1

#affiche la liste des device connectes | prints out device info at start
print(gamepad)
        

#we will import the RPi.GPIO library with the name of GPIO
import RPi.GPIO as GPIO
import pigpio
pi = pigpio.pi()
#we will set the pin numbering to the GPIO.BOARD numbering
#for more details check the guide attached to this code
GPIO.setmode(GPIO.BOARD)
#the next variable stores the pin used to control the speed of the motor
motorspeed_pin = 8
servo_pin = 17
#the next two variables store the pins used to control the direction of the motor
DIRA = 10
DIRB = 22
#the variable "delayOn" stores the time (in seconds) for the motor to remain On
delayOn = 2
#the variable "delayOff" stores the time (in seconds) for the motor to remain Off
delayOff = 1.5
#we will set the pins as output
GPIO.setup(motorspeed_pin, GPIO.OUT)
GPIO.setup(DIRA, GPIO.OUT)
GPIO.setup(DIRB, GPIO.OUT)
pi.set_mode(servo_pin, pigpio.OUTPUT)
#the motorspeed_pin will be used as an enable pin on the motor driver
pwmPIN = GPIO.PWM(motorspeed_pin, 100)
#we start the pwm instance with a duty cycle of 0
pwmPIN.start(0)
#define a function to stop the motor
def turnOff():
    #this instruction is used to set the speed of the motor to 0 (Off)
     pwmPIN.ChangeDutyCycle(0)
     #in these instructions the state is irrelevant because the speed is 0
     GPIO.output(DIRA, GPIO.LOW)
     GPIO.output(DIRB, GPIO.LOW)
     sleep(delayOff)
     
def powerMotor(speedPercentage, direction):
    pwmPIN.ChangeDutyCycle(speedPercentage if speedPercentage > 15 else 0)
    GPIO.output(DIRA, GPIO.HIGH if direction == 'left' else GPIO.LOW)
    GPIO.output(DIRB, GPIO.HIGH if direction == 'right' else GPIO.LOW)

def setServo(degrees):
    servoMax = 2500
    servoMin = 500
    value = 500 + (degrees * ((servoMax- servoMin)/180))
    print('setServo', value)
    pi.set_servo_pulsewidth(servo_pin, value)
    
def setServoController(value):
    setServo(180/analogMax*value)
     
     
try:
    for event in gamepad.read_loop():
        #Boutons | buttons 
        if event.type == ecodes.EV_KEY:
            print(event)
        
        #Gamepad analogique | Analog gamepad
        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            #print(absevent.event.code, absevent.event.value)
            
            if absevent.event.code == 1:
                direction = 'left' if absevent.event.value > analogMid else 'right'
                power = (abs(absevent.event.value - analogMid) / analogMid) * 100
                powerMotor(power, direction)
            elif absevent.event.code == 2:
                setServoController(absevent.event.value)
                
    
    
    
    while True:
        powerMotor(10, 'left')
        sleep(delayOn)
        #turn off the motor
        turnOff()
        
        powerMotor(10, 'right')
        sleep(delayOn)
        #turn off the motor
        turnOff()
        
        powerMotor(5, 'left')
        sleep(delayOn)
        #turn off the motor
        turnOff()
        
        powerMotor(5, 'right')
        sleep(delayOn)
        #turn off the motor
        turnOff()
except KeyboardInterrupt:
    pass
except:
    pass
    
pi.set_servo_pulsewidth(servo_pin, 0)
pi.stop()
#clean all the used ports
GPIO.cleanup()