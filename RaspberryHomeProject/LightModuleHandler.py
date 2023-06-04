from LightModule import LightModule
from AlarmClock import AlarmClock
import threading
import time
#from RelayModule import RelayModule

class LightModuleHandler:
    lightModeAllowed = False
    threadDisableNightLight = None
    threadEnableNightLightSoon = None
    intervalOfNightLightTime = (21, 7)

    @staticmethod
    def canEnableNightLight(hour):
        return hour >= LightModuleHandler.intervalOfNightLightTime[0] or hour < LightModuleHandler.intervalOfNightLightTime[1]
    
    @staticmethod
    def sumOfIntervalInMinutes():
        return (24 - AlarmClock.getHour() + LightModuleHandler.intervalOfNightLightTime[1]) * 60

    @staticmethod
    def initializeNightLight():
        if LightModuleHandler.canEnableNightLight(AlarmClock.getHour()) == True:
            sumOfMinutes = AlarmClock.sumUntilTimeInMinutes(LightModuleHandler.intervalOfNightLightTime[1], 0, AlarmClock.getHour(), AlarmClock.getMinute())
            LightModuleHandler.threadDisableNightLight = threading.Timer(sumOfMinutes * 60, LightModuleHandler.disableNightLight)
            LightModuleHandler.threadDisableNightLight.start()
            LightModuleHandler.lightModeAllowed = True
            hours = int(int(sumOfMinutes) / 60)
            minutes = int(int(sumOfMinutes) % 60)
            #RelayModule.switchOn()
            LightModule.initializeLight()
            print('light module activated for ' + str(hours) + ' hours and ' + str(minutes) + ' minutes...')
        else:
            #print(LightModuleHandler.sumUntilTimeInMinutes())
            sumOfMinutes = AlarmClock.sumUntilTimeInMinutes(LightModuleHandler.intervalOfNightLightTime[0], 0, AlarmClock.getHour(), AlarmClock.getMinute())
            LightModuleHandler.threadEnableNightLightSoon = threading.Timer(sumOfMinutes * 60, LightModuleHandler.initializeNightLight)
            LightModuleHandler.threadEnableNightLightSoon.start()
            hours = int(int(sumOfMinutes) / 60)
            minutes = int(int(sumOfMinutes) % 60)
            print('light module initial execution sheduled in ' + str(hours) + ' hours and ' + str(minutes) + ' minutes...')

    @staticmethod
    def turnOnLight():
        if LightModuleHandler.lightModeAllowed and not LightModule.isLit():
            LightModule.toggleWithLightModule()

    @staticmethod
    def disableNightLight():
        LightModuleHandler.lightModeAllowed = False
        print('light module disabled')
        LightModuleHandler.initializeNightLight() # set timer for restart by calling
        #RelayModule.switchOff()
