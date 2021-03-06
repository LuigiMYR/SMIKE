#!/usr/bin/env python
# -*- coding: utf-8 -*-



import time, collections, RPi.GPIO as GPIO, os, sys
from omxplayer import OMXPlayer

if os.path.exists("/home/pi/SMIKE/Smike.pid"):
    sys.exit(0)
else:
    open("/home/pi/SMIKE/Smike.pid", "w").close()

ReedBeatPin = 4
ReedBrakePin = 17
LEDPin = 18


SongDict = collections.OrderedDict()


def UpdateFrequency(channel):
    global Time, ActualFrequency
    if time.time() - Time > Bias:
        ##Frequency Check
        #print("CONTACT")
        
        Tmp = time.time()
        PeriodTime = Tmp - Time
        Time = Tmp
        ActualFrequency = 1/PeriodTime*60*2
        global logfile
        logfile.write(str(ActualFrequency)+"; ")
        
       

def UpdateSong(SongId):
    global Fading
    Fading = True
    
def OnBrakeRising(channel):
    GPIO.output(LEDPin,GPIO.LOW)
    GPIO.remove_event_detect(ReedBrakePin)
    GPIO.add_event_detect(ReedBrakePin, GPIO.FALLING, callback=OnBrakeFalling)
    #print("OFF")
def OnBrakeFalling(channel):
    GPIO.output(LEDPin,GPIO.HIGH)
    GPIO.remove_event_detect(ReedBrakePin)
    GPIO.add_event_detect(ReedBrakePin, GPIO.RISING, callback=OnBrakeRising)
    #print("OFF")





GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ReedBeatPin, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(ReedBrakePin, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(LEDPin, GPIO.OUT)

GPIO.add_event_detect(ReedBeatPin, GPIO.RISING, callback=UpdateFrequency)

GPIO.add_event_detect(ReedBrakePin, GPIO.FALLING, callback=OnBrakeFalling)

##Frequency
PeriodTime = 0
Time = time.time()
Frequency = 1
ActualFrequency = 1


##User Data
Tolerance = 10
MinSongTime = 10
MinSongTimeRatio = 20
PushFactor = 1.05
Bias = 0.2
BlendSpeed = 5
Volume = CurrentVolume = -1100

##Song Data
CurrentSong = 1
LastSongStart = Time
Fading = False
SongUpdated = False

##SongDict Import
import csv
reader = csv.reader(open('/home/pi/SMIKE/Playlist.csv', 'r'))
Header = []
is_Header = True
for row in reader:
    if is_Header:
        Header = row
        is_Header = False
    else:
        SongDict[int(row[0])] = {}
        for index in range(1, len(Header)):
            
            if Header[index] == "BPM":
                SongDict[int(row[0])][Header[index]] = int(row[index])
            else:
                SongDict[int(row[0])][Header[index]] = row[index]


Song = (SongDict[1]["Title"]+'.mp3')
player = OMXPlayer('/home/pi/Music/' + Song)
logfile = open("/home/pi/SMIKE/Log.txt", "w")
try:
    #UpdateSong(1)
    
    player.play()
    player.set_volume(CurrentVolume)
    
    ##Tick
    while True:
        ##Frequqncy Interpolation
       
        
        Frequency += (ActualFrequency-Frequency)*0.025
        Frequency = min(Frequency, 4000)
        #print(Frequency)
        ##print(int(Frequency), MinSongTimeRatio * (Tolerance/abs(Frequency - SongDict[CurrentSong]["BPM"]))**0.066)
        ##Song Update
        if Fading:
            LastSongStart = time.time()
            if not SongUpdated:
                CurrentVolume = max(-3333, CurrentVolume - 100*BlendSpeed)
                
                if CurrentVolume == -3333:
                    SongUpdated = True
            else:
                if CurrentVolume == -3333:
                    player.quit()
                    player = OMXPlayer('/home/pi/Music/' + (SongDict[CurrentSong]["Title"]+'.mp3'))
                    player.play()
                    
            
                CurrentVolume = min(Volume, CurrentVolume + 100*BlendSpeed)
                
                if CurrentVolume == Volume:
                    SongUpdated = Fading = False
                    
                    
            player.set_volume(CurrentVolume)
            print(CurrentVolume, CurrentSong)
            
            
            
        elif SongDict[CurrentSong]["BPM"] - Tolerance < Frequency < SongDict[CurrentSong]["BPM"] + Tolerance:
            pass
        else:
            CurrentDelta = Frequency - SongDict[CurrentSong]["BPM"]
            
            MinSongTime = MinSongTimeRatio * (Tolerance/abs(CurrentDelta))**0.1
            
            if time.time() - LastSongStart > MinSongTime:
                OldSong = CurrentSong
                if CurrentDelta > 0:
                    while CurrentSong < len(SongDict) and abs(Frequency - SongDict[CurrentSong+1]["BPM"]) <= abs(Frequency - SongDict[CurrentSong]["BPM"])*PushFactor:
                        CurrentSong += 1
                    if OldSong != CurrentSong:
                        UpdateSong(CurrentSong)
    
                elif CurrentDelta < 0 and CurrentSong != 1:
                    while CurrentSong > 1 and abs(Frequency - SongDict[CurrentSong-1]["BPM"])*PushFactor <= abs(Frequency - SongDict[CurrentSong]["BPM"]):
                        CurrentSong -= 1
                    if OldSong != CurrentSong:
                        UpdateSong(CurrentSong)
            else:
                pass
                #print("w8 m8 1337: ", MinSongTime - (time.time() - LastSongStart), MinSongTime, CurrentDelta)
       
except KeyboardInterrupt:
    player.quit()
    logfile.close()
    GPIO.output(LEDPin,GPIO.LOW)

            
