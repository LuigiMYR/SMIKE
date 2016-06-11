import time, collections, RPi.GPIO as GPIO
from omxplayer import OMXPlayer


ReedPin = 4 # INSERT NIPPLE HERE

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(ReedPin, GPIO.IN, GPIO.PUD_DOWN)



SongDict = collections.OrderedDict()


def UpdateFrequency(channel):
    
    if time.time() - Time > Bias:
        ##Frequency Check
        print("CONTACT")
        global Time, ActualFrequency
        Tmp = time.time()
        PeriodTime = Tmp - Time
        Time = Tmp
        ActualFrequency = 1/PeriodTime*60*2
        
       

def UpdateSong(SongId):
    global player, LastSongStart
    Song = (SongDict[SongId]["Title"]+'.mp3')
    player.quit()
    player = OMXPlayer('/home/pi/Music/' + Song)
    player.play()
    LastSongStart = time.time()

def QuitPlay():
    player.quit()


GPIO.add_event_detect(ReedPin, GPIO.RISING, callback=UpdateFrequency)

##Frequency
PeriodTime = 0
Time = time.time()
Frequency = 1
ActualFrequency = 1


##User Data
Tolerance = 5
MinSongTime = 10
PushFactor = 1.05
Bias = 0.2

##Song Data
CurrentSong = 1
LastSongStart = Time

##SongDict Import
import csv
reader = csv.reader(open('Playlist.csv', 'r'))
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
print(SongDict)


Song = (SongDict[1]["Title"]+'.mp3')
player = OMXPlayer('/home/pi/Music/' + Song)
try:
    UpdateSong(1)
    
    player.play()
    
    ##Tick
    while True:
        ##Frequqncy Interpolation
        if abs(Frequency-ActualFrequency) > Tolerance:
        
            Frequency += (ActualFrequency-Frequency)*0.1
            Frequency = min(Frequency, 400)
            print(int(Frequency))
            
            #print("CONTACT-----------------------------------------------------------", PeriodTime, Frequency, ActualFrequency)
            print(int(Frequency), PeriodTime)
            ##Song Update
            if SongDict[CurrentSong]["BPM"] - Tolerance < Frequency < SongDict[CurrentSong]["BPM"] + Tolerance:
                pass
            elif time.time() - LastSongStart > MinSongTime:
                CurrentDelta = Frequency - SongDict[CurrentSong]["BPM"]
                if CurrentDelta > 0 and CurrentSong < len(SongDict):
                    NewDelta = Frequency - SongDict[CurrentSong+1]["BPM"]
                    if abs(NewDelta) <= abs(CurrentDelta)*PushFactor:
                        CurrentSong += 1
                        print("CRASHPOINT")
                        UpdateSong(CurrentSong)
    
                elif CurrentDelta < 0 and CurrentSong != 1:
                    NewDelta = Frequency - SongDict[CurrentSong-1]["BPM"]
                    if abs(NewDelta)*PushFactor <= abs(CurrentDelta):
                        CurrentSong -= 1
                        UpdateSong(CurrentSong)
            else:
                print("w8 m8 1337: ",time.time() - LastSongStart)
        
       
except KeyboardInterrupt:
    player.quit()
        
            
            
