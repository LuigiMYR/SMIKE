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
    #global player, LastSongStart
    #Song = (SongDict[SongId]["Title"]+'.mp3')
    #player.quit()
    #player = OMXPlayer('/home/pi/Music/' + Song)
    #player.play()
    #LastSongStart = time.time()
    global Fading
    Fading = True
    
def QuitPlay():
    player.quit()


GPIO.add_event_detect(ReedPin, GPIO.RISING, callback=UpdateFrequency)

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
BlendSpeed = 1
CurrentVolume = 0
Volume = -1000

##Song Data
CurrentSong = 1
LastSongStart = Time
Fading = False
SongUpdated = False

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


Song = (SongDict[1]["Title"]+'.mp3')
player = OMXPlayer('/home/pi/Music/' + Song)
try:
    #UpdateSong(1)
    
    player.play()
    player.set_volume(CurrentVolume)
    
    ##Tick
    while True:
        ##Frequqncy Interpolation
       
        
        Frequency += (ActualFrequency-Frequency)*0.025
        Frequency = min(Frequency, 400)
        
        print(int(Frequency), MinSongTimeRatio * (Tolerance/abs(Frequency - SongDict[CurrentSong]["BPM"]))**0.1)
        ##Song Update
        if Fading:
            print(CurrentVolume)
            if not SongUpdated:
                CurrentVolume = max(-3333, CurrentVolume - 100*BlendSpeed)
                
                if CurrentVolume == -3333:
                    SongUpdated = True
            else:
                if CurrentVolume == -3333:
                    Song = (SongDict[CurrentSong]["Title"]+'.mp3')
                    player.quit()
                    player = OMXPlayer('/home/pi/Music/' + Song)
                    player.play()
            
                CurrentVolume = min(Volume, CurrentVolume + 100*BlendSpeed)
                
                if CurrentVolume == Volume:
                    SongUpdated = Fading = False
                    LastSongStart = time.time()
                    
            player.set_volume(CurrentVolume)
            
            
            
        elif SongDict[CurrentSong]["BPM"] - Tolerance < Frequency < SongDict[CurrentSong]["BPM"] + Tolerance:
            pass
        else:
            CurrentDelta = Frequency - SongDict[CurrentSong]["BPM"]
            
            MinSongTime = MinSongTimeRatio * (Tolerance/abs(CurrentDelta))**2
            
            if time.time() - LastSongStart > MinSongTime:
                
                if CurrentDelta > 0 and CurrentSong < len(SongDict):
                    NewDelta = Frequency - SongDict[CurrentSong+1]["BPM"]
                    if abs(NewDelta) <= abs(CurrentDelta)*PushFactor:
                        CurrentSong += 1
                        UpdateSong(CurrentSong)
    
                elif CurrentDelta < 0 and CurrentSong != 1:
                    NewDelta = Frequency - SongDict[CurrentSong-1]["BPM"]
                    if abs(NewDelta)*PushFactor <= abs(CurrentDelta):
                        CurrentSong -= 1
                        UpdateSong(CurrentSong)
            else:
                pass
                #print("w8 m8 1337: ", MinSongTime - (time.time() - LastSongStart), MinSongTime, CurrentDelta)
    time.sleep(0.16667/2)
       
except KeyboardInterrupt:
    player.quit()
        
            
            
