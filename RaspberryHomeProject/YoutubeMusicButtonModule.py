from PinModule import PinModule
from PinModes import PinModes
import RPi.GPIO as GPIO
from Pins import Pins

class YoutubeMusicButtonModule:

    @staticmethod
    def initializedButton():   
        PinModule.pinModePup(Pins.PIN_BUTTON_YOUTUBE_MUSIC, PinModes.PUP_UP)

    @staticmethod
    def getButtonState():
        return not (PinModule.readInput(Pins.PIN_BUTTON_YOUTUBE_MUSIC) == 1)
