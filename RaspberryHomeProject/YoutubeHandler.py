from FileHandler import FileHandler
import webbrowser
import threading
import time
import contextlib
import urllib.request
import os
import json
from random import randint
import requests

class YoutubeHandler:
    def __init__(self):
        self.isYoutubeMode = False
        self.videoFileHandler = FileHandler('youtubeVideoPlaylist.txt')
        self.musicFileHandler = FileHandler('youtubeMusicPlaylist.txt')

        # Minecraft LP specified
        self.videoNotionFlag = 'Minecraft #'
        self.durationNotionFlag = 'Dauer: '

        self.futureVideoLinkSubstring = None
        self.threadNextVideoQueue = None
        self.threadDurationOfYoutubeMode = None
        self.durationOfYoutubeMode = 25 # 30 * 60
        self.videoStartTime = None

        # fullscreen alternative
        self.YOUTUBE_STANDARD_LINK = 'https://www.youtube.com'
        self.YOUTUBE_EMBED_TEMPLATE_START = self.YOUTUBE_STANDARD_LINK + '/embed/'
        self.YOUTUBE_EMBED_TEMPLATE_END = '?rel=0&autoplay=1&start='

        # set music mode on default
        self.modeFlag = 'music'
        self.currentMusicLink = None

        self.timeFlag = '&t='

    def getYoutubeMode(self):
        return self.isYoutubeMode

    def setYoutubeMode(self, mode):
        self.isYoutubeMode = mode
        
    def getVideoID(self, linkO):
        index = linkO.find('v=')
        link = linkO[index+2:]
        index = link.find('&t=')
        
        if index != -1:
            link = link[:index]
            
        return link

    def startBrowser(self, link):
        #chromium = webbrowser.get('/usr/bin/chromium-browser')
        videoStartTime = 0
        videoStartIndex = link.find('&t=')
        if videoStartIndex != -1:
            videoStartTime = link[videoStartIndex+3:]
            
        link = self.getVideoID(link)
        
        newLink = self.YOUTUBE_EMBED_TEMPLATE_START + link + self.YOUTUBE_EMBED_TEMPLATE_END + str(videoStartTime)
            
        #chromium.open_new_tab(newLink)

        webbrowser.open_new_tab(newLink)

    def grabNextVideoLinkAndThread(self, link, currentVideoDuration = None):
        with contextlib.closing(urllib.request.urlopen(link)) as response:
           html = response.read()
        html = html.decode()
        iterator = None
        #find current video
        index = html.find(self.videoNotionFlag) 
        if index != -1:
            i = index + len(self.videoNotionFlag)
            iterator = int(html[i:i + 3]) + 1
            i = i + len(str(iterator))
            #find next video
            index = html.find(self.videoNotionFlag + str(iterator))
            s_href = 'href="'
            hrefIndex = html[index:].find('href="') + len(s_href)
            buggyIndex = html[index+hrefIndex:].find('"')
            self.futureVideoLinkSubstring = str(html[index+hrefIndex:index+hrefIndex+buggyIndex])
            print(self.futureVideoLinkSubstring)
            
            if currentVideoDuration == None:
                index = index + html[index:].find(self.durationNotionFlag) + len(self.durationNotionFlag)
                secondsFlagIndex = index+html[index:].find(':')
                minuteValueOfVideo = html[index:secondsFlagIndex]
                secondValueOfVideo = html[secondsFlagIndex+1:secondsFlagIndex+1+2]
                currentVideoDuration = int(secondValueOfVideo) + int(minuteValueOfVideo) * 60
            else:
                link = self.videoFileHandler.checkFile()
                index = link.find('&t=')
                if index != -1:
                    try:
                        currentVideoDuration -= int(link[index+3:])
                        print('Remaining duration: ' + str(int(currentVideoDuration / 60)) + ':' + str(currentVideoDuration % 60))
                    except ValueError:
                        raise ValueError('cannot read start time from file link')
            self.threadNextVideoQueue = threading.Timer(currentVideoDuration, self.restartBrowserWithNextLink)
            self.threadNextVideoQueue.start()
        else:
            raise NameError('could not find html index!')

    def nextMusic(self):
        # restore link without time index in file
        originalLink = self.currentMusicLink[self.currentMusicLink.find('&t='):]
        self.musicFileHandler.swapLine(self.currentMusicLink, originalLink)

        # obtain next link and duration
        currentLink = self.currentMusicLink = self.getNextMusicLink()
        currentVideoDuration = self.getActualDurationOfVideo(currentLink)

        # setup video timer
        self.setupMusicThread(currentVideoDuration)

        self.startBrowser(link)

    def nextVideo(self):
        link = self.YOUTUBE_STANDARD_LINK + self.futureVideoLinkSubstring
        self.fileHandler.overrideFile(link)
        self.grabNextVideoLinkAndThread(link)
        self.startBrowser(link)
    
    def restartBrowserWithNextLink(self):
        self.closeBrowser()
        self.videoStartTime = int(time.time())

        if self.modeFlag == 'video':
            self.nextVideo()
        elif self.modeFlag == 'music':
            self.nextMusic()
        else:
            raise Exception('modeFlag is not valid again')
            
    def closeBrowser(self):
        os.system("pkill chromium")
    
    def disableMusic(self, deltaTime):
        oldProgressFlag = self.currentMusicLink.find(self.timeFlag)

        if oldProgressFlag == -1:
            # add time flag to link
            link = self.currentMusicLink + self.timeFlag + str(deltaTime)
            self.musicFileHandler.swapLine(self.currentMusicLink, link)
        else:
            # add progress to existing time flag
            oldProgress = int(self.currentMusicLink[oldProgressFlag + len(self.timeFlag):])
            currentProgress = oldProgress + deltaTime
            newLink = self.currentMusicLink[:oldProgressFlag + len(self.timeFlag)] + str(currentProgress)
            self.musicFileHandler.swapLine(self.currentMusicLink, newLink)

    def disableVideo(self, deltaTime):
        oldLink = self.videoFileHandler.checkFile()

        oldProgressFlag = oldLink.find(self.timeFlag)

        if oldProgressFlag == -1:
            # add time flag to link
            self.videoFileHandler.appendToFile(self.timeFlag + str(deltaTime))
        else:
            # add progress to existing time flag
            oldProgress = int(oldLink[oldProgressFlag + len(self.timeFlag):])
            currentProgress = oldProgress + deltaTime
            newLink = oldLink[:oldProgressFlag] + str(currentProgress)
            self.videoFileHandler.overrideFile(newLink)

    def disableYoutubeMode(self):
        # -15 seconds browser loading delay
        deltaTime = int(time.time()) - self.videoStartTime - 15

        # write the current time flag 
        if self.modeFlag == 'music':
            self.disableMusic(deltaTime)
        elif self.modeFlag == 'video':
            self.disableVideo(deltaTime)
        else:
            raise Exception('modeFlag is laggy everywhere')

        # canceling thread
        self.threadNextVideoQueue.cancel()
        self.closeBrowser()
        print('thread canceled: ' + str(self.threadNextVideoQueue))
        self.setYoutubeMode(False)
        print('youtube mode has been disabled!')

    def getNextMusicLink(self):
        lines = self.musicFileHandler.lineCount()
        randNum = randint(0, lines - 1)
        return self.musicFileHandler.getLineByIndex(randNum)

    def getActualDurationOfVideo(self, link):
        videoID = self.getVideoID(link)
        apiKey = "AIzaSyADbd4cqggfPHVBNvp2BnhDSMmJdoDAAz8"
        searchUrl = "https://www.googleapis.com/youtube/v3/videos?id="+videoID+"&key="+apiKey+"&part=contentDetails"
        response = requests.get(searchUrl).text#urllib.request.urlopen(searchUrl).read()
        data = json.loads(response)
        #print(response)
        items = data['items']
        contentDetails = items[0]['contentDetails']
        duration = contentDetails['duration']
        
        actualDuration = 0
        
        indexH = duration.find('H')
        indexM = duration.find('M')
        indexS = duration.find('S')
        
        if indexH != -1:
            actualDuration += int(duration[2:indexH]) * 60 * 60
            
            if indexM != -1:
                actualDuration += int(duration[indexH+1:indexM]) * 60
                
                if indexS != -1:
                    actualDuration += int(duration[indexM+1:indexS])
                    
        elif indexM != -1:
            actualDuration += int(duration[2:indexM]) * 60
                
            if indexS != -1:
                actualDuration += int(duration[indexM+1:indexS])
        
        return actualDuration

    def setupYoutubeDurationLimitation(self):
        self.threadDurationOfYoutubeMode = threading.Timer(self.durationOfYoutubeMode, self.disableYoutubeMode)
        self.threadDurationOfYoutubeMode.start()
        self.setYoutubeMode(True)
        print('youtube mode has been initialized!')

    def setupMusicThread(self, duration):
        self.threadNextVideoQueue = threading.Timer(duration, self.restartBrowserWithNextLink)
        self.threadNextVideoQueue.start()
        
    def initMusic(self):
        
        link = self.currentMusicLink = self.getNextMusicLink()

        self.startBrowser(link)

        # remember start time for video duration messure
        self.videoStartTime = int(time.time())

        currentVideoDuration = self.getActualDurationOfVideo(link)

        self.setupMusicThread(currentVideoDuration)

        self.setupYoutubeDurationLimitation()

    def initVideo(self):
        
        link = self.videoFileHandler.checkFile()

        self.startBrowser(link)
        
        self.videoStartTime = int(time.time())

        currentVideoDuration = self.getActualDurationOfVideo(link)

        self.grabNextVideoLinkAndThread(link, currentVideoDuration)
        
        self.setupYoutubeDurationLimitation()

    def initializeYoutubeMode(self, modeFlag = 'music'):
        self.modeFlag = modeFlag

        if self.modeFlag == 'music':
            self.initMusic()
        elif self.modeFlag == 'video':
            self.initVideo()
        else:
            raise Exception('youtube mode spec not found')

y = YoutubeHandler()
for i in range(6):
    y.initializeYoutubeMode('video')
    while y.getYoutubeMode() == True:
        pass
