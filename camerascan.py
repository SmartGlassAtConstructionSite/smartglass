import RPi.GPIO as GPIO
import time
import picamera
import datetime

swPin=14

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

oldSw=0
newSw=0

camera=picamera.PiCamera()
camera.resolution=(1024,768)

try:
    while True:
        newSw=GPIO.input(swPin)
        if newSw !=oldSw:
            oldSw=newSw
            
            if newSw==1:
                now=datetime.datetime.now()
                print(now)
                filename=now.strftime('%Y-%m-%d %H:%M:%S')
                camera.capture(filename+ '.jpg')
                
            time.sleep(0.2)

except KeyboardInterrupt:
    pass

GPIO.cleanup()        
