import threading
import time
import pygame

class AlarmClock:
    def __init__(self, timerEnabled, wakeHour = None, wakeMinute = None):
        self.timerEnabled = timerEnabled
        self.alarmHour = wakeHour
        self.alarmMinute = wakeMinute
        self.deltaHours = 0
        self.deltaMinutes = 0
        self.clockThread = None
        if self.timerEnabled == True:
            if self.alarmHour == None or self.alarmMinute == None:
                raise ValueError('constructor has not been specified!')
            self.enableAlert(self.timerEnabled)

    @staticmethod 
    def getHour():
        return int(time.strftime("%H"))

    @staticmethod 
    def getMinute():
        return int(time.strftime("%M")) 

    @staticmethod
    def sumOfIntervalInMinutes():
        return (24 - AlarmClock.getHour() + LightModuleHandler.intervalOfNightLightTime[1]) * 60

    @staticmethod
    def sumUntilTimeInMinutes(th, tm, h, m):
        
        difH = 0
        difM = 0

        if tm >= m:
            difM = tm - m
        else:
            difH = -1
            difM = 60 - m + tm
        
        if th >= h:
            difH += th - h
        else:
            difH += 24 - h + th
            
        if difH < 0:
            difH += 24

        if difH < 0 or difM < 0:
            raise ValueError('negative time')

        return difH * 60 + difM

    def wakeupLoop(self):
        print('playing alert...')
        pygame.mixer.init()
        pygame.mixer.music.load('island.mp3')
        while True:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

    def enableAlert(self, timerEnabled):
        self.timerEnabled = timerEnabled

        if self.timerEnabled == False:
            return False

        print('initializing clock...')
        
        sumOfMinutes = AlarmClock.sumUntilTimeInMinutes(self.alarmHour, self.alarmMinute, AlarmClock.getHour(), AlarmClock.getMinute())
        self.deltaHours = int(sumOfMinutes / 60)
        self.deltaMinutes = sumOfMinutes % 60
        self.clockThread = threading.Timer(sumOfMinutes * 60, self.wakeupLoop)
        self.clockThread.start()
        print('alert set in ' + str(self.deltaHours) + ' hours and ' + str(self.deltaMinutes) + ' minutes')
        
