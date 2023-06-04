from PinModule import PinModule
from Pins import Pins
from PinModes import PinModes

class RelayModule:
    
    @staticmethod
    def switchOn():
        PinModule.pinMode(Pins.PIN_OUT_RELAY, PinModes.OUT)
        
    @staticmethod
    def switchOff():
        PinModule.pinMode(Pins.PIN_OUT_RELAY, PinModes.IN)