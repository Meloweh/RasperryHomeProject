from YoutubeVideoButtonModule import YoutubeVideoButtonModule
from YoutubeMusicButtonModule import YoutubeMusicButtonModule
from YoutubeHandler import YoutubeHandler

class ButtonModuleHandler:
    youtubeHandler = YoutubeHandler()

    @staticmethod
    def initializeAllButtons():
        YoutubeVideoButtonModule.initializedButton()
        YoutubeMusicButtonModule.initializedButton()

    @staticmethod
    def updateAllButtons():
        ButtonModuleHandler.updateYoutubeButton()

    @staticmethod
    def updateYoutubeButton():
        if ButtonModuleHandler.youtubeHandler.getYoutubeMode() == False:
            if YoutubeVideoButtonModule.getButtonState() == True:
                print('initializing youtube video mode...')
                ButtonModuleHandler.youtubeHandler.initializeYoutubeMode()
                
            if YoutubeMusicButtonModule.getButtonState() == True:
                print('initializing youtube music mode...')
                ButtonModuleHandler.youtubeHandler.initializeYoutubeMode('music')
                
        
                

    
