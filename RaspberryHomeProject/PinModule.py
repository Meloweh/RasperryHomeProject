import wiringpi
from Outputs import Outputs

class PinModule:
    wiringpi.wiringPiSetupGpio()
        
    @staticmethod
    def pinMode(pin, mode):
        wiringpi.pinMode(pin, mode)

    @staticmethod
    def pinModePup(pin, mode):
        wiringpi.pullUpDnControl(pin, mode)
    
    @staticmethod
    def readInput(pin):
        return wiringpi.digitalRead(pin) == Outputs.HIGH

    @staticmethod
    def writeOutput(pin, output):
        wiringpi.digitalWrite(pin, output)

