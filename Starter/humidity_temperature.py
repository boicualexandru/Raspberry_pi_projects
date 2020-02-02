#import the libraries
import RPi.GPIO as GPIO
import Adafruit_DHT
GPIO.setmode(GPIO.BCM)
#name the type of sensor used
type = Adafruit_DHT.DHT11
#declare the pin used by the sensor in GPIO form
dht11 = 25
#set the sensor as INPUT
GPIO.setup(dht11, GPIO.IN)

try:
    while True:
        #make the reading
        humidity, temperature = Adafruit_DHT.read_retry(type, dht11)
        #we will display the values only if they are not null
        if humidity is not None and temperature is not None:
            print('Temperature = {:.1f} Humidity = {:.1f}' .format(temperature, humidity))
except KeyboardInterrupt:
    pass
#clean all the used ports
GPIO.cleanup()