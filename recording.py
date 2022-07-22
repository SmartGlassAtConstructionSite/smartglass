import RPi.GPIO as GPIO
import time
import pyaudio
import wave
import datetime

swPin=14

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(swPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

oldSw=0
newSw=0

CHUNK=1024
FORMAT=pyaudio.paInt16
CHANNELS=1
RATE=44100
SAMPLE_SIZE=2
RECORD_SECONDS=10

def saveVoice():
    p=pyaudio.PyAudio()
    
    stream=p.open(format=FORMAT,
                         channels=CHANNELS,
                         rate=RATE, 
                         input=True,
                         frames_per_buffer=CHUNK)
    
    print("Start to record the audio." )

    frames=[]
    
    now=datetime.datetime.now()
    fileName = now.strftime('%Y-%m-%d %H:%M:%S')
    
    for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
        data=stream.read(CHUNK)
        frames.append(data)
        
    print("Recording is finished. ")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf=wave.open(fileName+ '.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b' ' .join(frames))
    wf.close()
    
try: 
    while True:
        newSw=GPIO.input(swPin)
        if newSw != oldSw:
            oldSw = newSw
            
        if newSw == 1:
            saveVoice()
            
        time.sleep(0.2)
        
except KeyboardInterrupt:
    pass

GPIO.cleanup()
