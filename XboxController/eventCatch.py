#import evdev
from evdev import InputDevice, categorize, ecodes
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)

try:
    #cree un objet gamepad | creates object gamepad
    gamepad = InputDevice('/dev/input/event0')

    #affiche la liste des device connectes | prints out device info at start
    print(gamepad)

    #affiche les codes interceptes |  display codes
    for event in gamepad.read_loop():
        #Boutons | buttons 
        if event.type == ecodes.EV_KEY:
            print(event)
        
        if event.code == 304:
            if event.value == 1:
                GPIO.output(8, GPIO.HIGH)
            else:
                GPIO.output(8, GPIO.LOW)
        
        #Gamepad analogique | Analog gamepad
        elif event.type == ecodes.EV_ABS:
            absevent = categorize(event)
            print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")
except:
   print("some error") 
finally:
   print("clean up") 
   GPIO.cleanup() # cleanup all GPIO 