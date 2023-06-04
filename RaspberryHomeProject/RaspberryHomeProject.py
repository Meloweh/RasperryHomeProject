from AlarmClock import AlarmClock
from ButtonModuleHandler import ButtonModuleHandler
from PirModule import PirModule
import time

class Main:
    MAIN_LOOP_DELAY = 0.5
    
    def __init__(self):
        self.alert = AlarmClock(True, 7, 29)
        PirModule.initializePir()
        ButtonModuleHandler.initializeAllButtons()

    def update(self):
        ButtonModuleHandler.updateAllButtons()
        time.sleep(self.MAIN_LOOP_DELAY)
        

if __name__ == '__main__':
    main = Main()
    while True:
        main.update()
