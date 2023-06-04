from PinModule import PinModule
from Pins import Pins
from PinModes import PinModes
from Outputs import Outputs
from LightModuleHandler import LightModuleHandler
import time
import threading

class PirModule:
    STANDBY_LOOP_DELAY = 0.1
    timerPirDelay = None
    DELAY_TIME = 2 # seconds

    @staticmethod
    def initializePir():
        PinModule.pinMode(Pins.PIN_SENSOR_PIR, int(PinModes.IN))
        print('awaiting pir standby...')
        
        while PinModule.readInput(Pins.PIN_SENSOR_PIR) == True:
            time.sleep(PirModule.STANDBY_LOOP_DELAY)
        
        print('success!')
        LightModuleHandler.initializeNightLight()

        PirModule.timerPirDelay = threading.Timer(PirModule.DELAY_TIME, PirModule.updatePir)
        PirModule.timerPirDelay.start()

    @staticmethod
    def motionDetected():
        return PinModule.readInput(Pins.PIN_SENSOR_PIR)

    @staticmethod
    def updatePir():
        if PirModule.motionDetected() == True:
            print('motion detected')
            LightModuleHandler.turnOnLight()
            
        PirModule.timerPirDelay = threading.Timer(PirModule.DELAY_TIME, PirModule.updatePir)
        PirModule.timerPirDelay.start()
