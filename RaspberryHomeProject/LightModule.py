from RCModule import RCModule
import time
from PinModule import PinModule
from Pins import Pins
from PinModes import PinModes
from Outputs import Outputs
import threading

class LightModule:
    actionDurationBusynes = 60 * 3
    minimumCountDelay = 3000
    timerDisableLight = None
    islit = False

    @staticmethod
    def initializeLight():
        PinModule.pinMode(Pins.PIN_OUT_LIGHT, PinModes.OUT)
        PinModule.writeOutput(Pins.PIN_OUT_LIGHT, Outputs.LOW)

    @staticmethod
    def turnOnLight():
        PinModule.writeOutput(Pins.PIN_OUT_LIGHT, Outputs.HIGH)
        timerDisableLight = threading.Timer(LightModule.actionDurationBusynes, LightModule.disableLight)
        timerDisableLight.start()
        LightModule.islit = True
        print('light set on')

    @staticmethod
    def disableLight():
        PinModule.writeOutput(Pins.PIN_OUT_LIGHT, Outputs.LOW)
        LightModule.islit = False
        print('light set off')

    @staticmethod
    def isLit():
        return LightModule.islit

    @staticmethod
    def toggleWithLightModule(minimumCount = None):
        if minimumCount == None:
            minimumCount = LightModule.minimumCountDelay
        #LightModule.turnOnLight()
        RCModule.initializeSensor()
        #count = RCModule.countRCDelay()

        count = RCModule.countRCDelayTo(minimumCount)
        print('RC ticks: ' + str(count))
        if count <= LightModule.minimumCountDelay:
            LightModule.turnOnLight()
