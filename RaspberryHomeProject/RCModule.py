from PinModule import PinModule
import time
from Pins import Pins
from PinModes import PinModes
from Outputs import Outputs

class RCModule:

    @staticmethod
    def initializeSensor():
        PinModule.pinMode(Pins.PIN_SENSOR_RC, PinModes.OUT)
        
    @staticmethod
    def countRCDelayTo(maxCount = None):
        counter = 0
        PinModule.writeOutput(Pins.PIN_SENSOR_RC, Outputs.HIGH)
        time.sleep(1)
        PinModule.pinMode(Pins.PIN_SENSOR_RC, PinModes.IN)

        while PinModule.readInput(Pins.PIN_SENSOR_RC) == True:
            counter += 1
            if maxCount != None and counter > maxCount:
                return counter
        return counter
