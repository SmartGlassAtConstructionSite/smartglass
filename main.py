from picamera import PiCamera
from time import sleep
from datetime import datetime
import boto3
import RPi.GPIO as GPIO
import os
import curses
import pyaudio
import wave

swPin=14

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

ACCESS_KEY = 'access_key_ID'
SECRET_KEY = 'access_secret_key'

oldSw=0
newSw=0

CHUNK=262144
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=62500
SAMPLE_SIZE=1
RECORD_SECONDS=5

screen = curses.initscr()
curses.noecho()
curses.cbreak()
curses.halfdelay(3)

screen.keypad(True)

camera = PiCamera()
camera.resolution = (2592, 1944)


def detectusus():
    curtime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    #take picture
    camera.start_preview()
    sleep(0.2)
    savephotofile = '/home/pi/python/' + curtime + '.jpg'
    camera.capture(savephotofile)
    camera.stop_preview()
    
    #record location
    p=pyaudio.PyAudio()
    
    stream=p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE, 
                         input=True,
                         frames_per_buffer=CHUNK)
    
    print("Start to record the audio." )

    frames=[]
    
    now=datetime.now()
    
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data=stream.read(CHUNK)
        frames.append(data)
        
    print("Recording is finished. ")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    savaudiofile='/home/pi/python/' + curtime + '.mp4'
    
    wf=wave.open(savaudiofile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b' ' .join(frames))
    wf.close()
    
    #upload to AWS S3
    client = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)
    client.upload_file(savephotofile,'BucketName',curtime+'.jpg')
    client.upload_file(savaudiofile,'BucketName',curtime+'.mp4')
 
    print('Done')

try:
    while True:
        newSw=GPIO.input(swPin)
        if newSw !=oldSw:
            oldSw=newSw
            
            if newSw==1:
                now=datetime.now()
                detectusus()
            sleep(0.2)

except KeyboardInterrupt:
    pass

    GPIO.cleanup()
    camera.close()
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()
