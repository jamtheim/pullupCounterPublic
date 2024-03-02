# *********************************************************************************
# Author: Christian Jamtheim Gustafsson, PhD, Medical Physcist Expert
# Description: Class for support functions for the data pipeline for pullup counter. 
# *********************************************************************************
import numpy as np
import os
import random
import chime
from soco.discovery import by_name
import glob
import time 
# Load modules
from commonConfig import commonConfigClass
conf = commonConfigClass() 


class supportMethodsClass:
    """
    Class describing functions needed for data pipeline.
    """

    def __init__ (self):
        """
        Init function
        """
        pass


    def getRandomSoundFilePath(self, soundBasePathThemeLocal, soundBasePathWeb):
        """
        This function returns a random file path from the soundBasePathLocal folder.
        This is selcted from local data. 
        Data must also be available on a webserver.
        This is because SOCO can only play from a webadress and not directly from a local path.

        input: 
        soundBasePathThemeLocal: string, the path to the folder containing the sound files on local disk
        soundBasePathWeb: string, the webadress to the folder containing the sound files on the webserver
        """
        # Use glob to get all paths of all files in the directory. It could be wav or mp3 files.
        # For best compatibility, use mp3 files with SONOS. 
        # Use the '**' pattern to match all files in subdirectories. Requires mp3.
        # Recursive=True means that it will search in all subdirectories
        allSoundFilePathsLocal = glob.glob(os.path.join(soundBasePathThemeLocal, '**', '*.mp3'), recursive=True)
        # Remove all files containing the word "pappa" as these are only used for pullup counts
        allSoundFilePathsLocal = [x for x in allSoundFilePathsLocal if 'pappa' not in x]        
        # Select a random file from the list
        soundFilePathLocal = random.choice(allSoundFilePathsLocal)
        # Assert that the file exists
        assert os.path.exists(soundFilePathLocal), 'The path to the sound file does not exist'
        # Separate the path and get only the part after 'sounds'
        # We need to do this to get the webbadress to the file from the webserver
        soundFilePathGeneral = soundFilePathLocal.split('sounds')[1]
        # Add the webadress to the file path
        soundFilePathWeb = soundBasePathWeb + soundFilePathGeneral
        # Make sure all backslashes are replaced with forward slashes as this is a http adress
        soundFilePathWeb = soundFilePathWeb.replace('\\', '/')
        # Return the path to the file
        return soundFilePathWeb


    def getHASoundStatus(self):
        """
        This function returns the status of the Home Assistant pullup sound switch.
        """
        # Read the file with the switch status
        with open(conf.sonos.HASoundStatusFilePath, 'r') as f:
            # Read the status
            HASoundStatus = f.read()
            # Newline character included, use in
            if 'on' in HASoundStatus:
                HASoundStatusLogic = True
            else:
                HASoundStatusLogic = False
            # Return the status
            return HASoundStatusLogic
        

    def getHASoundTheme(self):
        """
        This function returns the theme of the Home Assistant pullup sound.
        """
        # Read the file with the switch status
        with open(conf.sonos.HASoundThemeFilePath, 'r') as f:
            # Read the status
            HASoundTheme = f.read()
            # Newline character included, use in
            if 'oora' in HASoundTheme:
                HASoundTheme = 'oora'
            if 'random' in HASoundTheme:
                HASoundTheme = 'random'
            # Return the status
            return HASoundTheme
    
    
    def getHASonosRoom(self):
        """
        This function returns the room of the Home Assistant Sonos selection
        """
        # Read the file with the switch status
        with open(conf.sonos.HASoundRoomFilePath, 'r') as f:
            # Read the status
            HASonosRoom = f.read()
            # Newline character included, use in
            if 'Koket' in HASonosRoom:
                HASonosRoom = 'Koket'
            if 'Uterummet' in HASonosRoom:
                HASonosRoom = 'Uterummet'
            if 'Kontoret' in HASonosRoom:
                HASonosRoom = 'Kontoret'
            # Return the status
            return HASonosRoom
                

    def getHASonosVolume(self): 
        """
        This function returns the volume of the Home Assistant Sonos selection
        """
        # Read the file with the switch status
        with open(conf.sonos.HASoundVolumeFilePath, 'r') as f:
            # Read the status
            HASonosVolume = int(f.read())
            # Should be equal to 10,20,30,40,50,60,70,80,90,100, assert this
            assert HASonosVolume in [10,20,30,40,50,60,70,80,90,100], 'Volume is not in the list [10,20,30,40,50,60,70,80,90,100]'
            # Return the status
            return HASonosVolume
    

    def playOnSonos(self, pullupCounts):
        """
        This function plays a sound, defined from a file, on the SONOS device.
        inputs:
        pullupCounts: int
            The pullup counter 
        """
        # Get the room to play sound in
        room = self.getHASonosRoom()
        # Define the speaker to play on using the room name and SOCO
        speaker = by_name(room)
        # Get the volume to play on
        volume = self.getHASonosVolume()
        # Print volume
        #print('Playing sound in room: ' + room + ' with volume ' + str(volume))

        #print('Playing sound in room: ' + room)
        if self.getHASoundTheme() == 'random':
            # Get a random sound file path
            soundFilePath = self.getRandomSoundFilePath(conf.sonos.soundBasePath, conf.sonos.soundBasePathWeb)
            # Print the sound file path
            #print('Playing sound from file: ' + soundFilePath)

        if self.getHASoundTheme() == 'oora': 
            # Set the path to the sound file oorah.mp3
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', 'oorah.mp3')
            soundFilePath = soundFilePath.replace('\\', '/')
            #print('Playing sound from file: ' + soundFilePath)

        # Override determined sound file if pullupCounts is 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, or 55
        if pullupCounts == 5: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '5pappa.mp3')
        if pullupCounts == 10: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '10pappa.mp3')
        if pullupCounts == 15: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '15pappa.mp3')
        if pullupCounts == 20: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '20pappa.mp3')
        if pullupCounts == 25: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '25pappa.mp3')
        if pullupCounts == 30: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '30pappa.mp3')
        if pullupCounts == 35: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '35pappa.mp3')
        if pullupCounts == 40: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '40pappa.mp3')
        if pullupCounts == 45: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '45pappa.mp3')
        if pullupCounts == 50: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '50pappa.mp3')
        if pullupCounts == 55: 
            soundFilePath = os.path.join('http://192.168.1.2/sounds/military', '55pappa.mp3')            
            
        # Set the mute status and volume 
        speaker.mute = False
        speaker.volume = volume
        # Print the sound file path
        speaker.play_uri(soundFilePath)
    

    def writeTimeStampFirstPullup(self, pullupTimeFirst):
        """
        This function writes the time stamps for first pullup
        """
        # Write time stamp to first file
        #print('Writing time stamps to first file')
        try: 
            with open(conf.base.pullupTimeFirstFilePath, 'w') as f:
                f.write(str(pullupTimeFirst))
        except Exception as e:
            print('Failed to write time stamps to file')
            print(e)


    def writeTimeStampLastPullup(self, pullupTimeLast):
        """
        This function writes the time stamps for last pullup
        """
        # Write time stamp to last file
        #print('Writing time stamps to last file')
        try: 
            with open(conf.base.pullupTimeLastFilePath, 'w') as f:
                f.write(str(pullupTimeLast))
        except Exception as e:
            print('Failed to write time stamps to file')
            print(e)


    def pullupCounterAdd(self, pullupCounts, beenUp, beenDown):
        """
        Function to add a pullup to pullup counter if conditions are met.
        Conditions helps to avoid double counting of pullups when object is above the bar.

        pullupCounts: int
            Pullup counter
        beenUp: bool
            Flag if athlete has been above bar
        beenDown: bool
            Flag if athlete has been below bar
        """
        # Add pullup if conditions are met
        if (beenUp == True and beenDown == True):
            # Get time point of pullup
            now = time.localtime()
            # Format into string
            nowString = time.strftime("%Y-%m-%d %H:%M:%S", now)

            # Check if pullupCountsFilePath has a 0 after being reset
            # If so, set pullupCounts in this counter to 0
            with open(conf.base.pullupCountsFilePath, 'r') as f:
                pullupCountsFromFile = int(f.read())
                if pullupCountsFromFile==0: 
                    print('Pullup counter was reset, setting it to 0')
                    pullupCounts = 0

            # If this is the first pullup store it in a new variable
            if pullupCounts == 0:
                pullupTimeFirst = nowString
                pullupTimeLast = nowString
                # Write time stamps to file
                self.writeTimeStampFirstPullup(pullupTimeFirst)
                self.writeTimeStampLastPullup(pullupTimeLast)
            # If this is not the first pullup, store it in the last pullup variable
            if pullupCounts >= 1:
                pullupTimeLast = nowString
                self.writeTimeStampLastPullup(pullupTimeLast)

            # Add to pullup counter
            pullupCounts = pullupCounts + 1

            # Play randomize sound on SONOS
            # put it in try/except to avoid error for missing network access
            try: 
                if conf.data.playSonos==True and self.getHASoundStatus()==True:
                    #print('Playing sound on SONOS')
                    self.playOnSonos(pullupCounts)
            except Exception as e:
                print('Failed to play sound on SONOS')
                print(e)

            # Write pullup counter to file
            with open(conf.base.pullupCountsFilePath, 'w') as f:
                f.write(str(pullupCounts))
            # Play a beep
            if conf.data.playSound==True:
                chime.theme(conf.data.soundTheme)
                chime.success()
            beenUp = True
            beenDown = False

            # Print total pullups
            #print('Total pullups so far is ' + str(pullupCounts))
            #print(' ')
        
        # Return pullup counter and flags
        return pullupCounts, beenUp, beenDown
    

    def deleteVideoWhenNeeded(self, videoFilePath): 
        """
        Video file created from annotated stream should not be too big, make sure it is deleted with regular intervals. 
        Get seconds of current time and delete video file if it is 0 or 1 seconds
        This decreases the reading of the file size from every frame to twice every minute only
        """
        now = time.localtime()
        # Check if it is 0 or 1 seconds
        if (now.tm_sec == 0 or now.tm_sec == 1):
            # Check if video exist
            if os.path.exists(videoFilePath):
                # Get the size of the video file
                videoFileSize = os.path.getsize(videoFilePath)
                # If the file is bigger than 1000 MB, delete it
                if (videoFileSize > conf.data.maxVideoFileSize):
                    os.remove(videoFilePath)
            
