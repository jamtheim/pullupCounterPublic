# *********************************************************************************
# Author: Christian Jamtheim Gustafsson, PhD, Medical Physcist Expert
# Description: Configuration file for the data pipeline for pullup counter. 
# *********************************************************************************
import os
import numpy as np

class commonConfigClass():
    """
    Class describing the common configuration used in the project.
    Defines what configuration settings are used.
    """

    def __init__ (self):
        """
        Init function
        """
        pass
    
    class baseConfig:
        """
        Empty class to define base configuration
        """
        pass

    class dataConfig:
        """
        Empty class to define data configuration
        """
        pass

    class sonosConfig:
        """
        Empty class to define SONOS configuration
        """
        pass

   
    # Init base configuration class
    base = baseConfig()
    # Init data configuration class
    data = dataConfig()
    # Init organ configuration class
    sonos = sonosConfig()

    ### Base configuration ###
    # Set script path
    base.scriptPath = os.path.dirname(os.path.abspath(__file__))
    # Set file name and path for saving pullup counts
    base.pullupCountsFileName = 'pullupCounts.txt'
    # Make sure folder exist in scriptPath for saving pullup counts
    if not os.path.exists(os.path.join(base.scriptPath, 'data')):
        os.makedirs(os.path.join(base.scriptPath, 'data'))

    # Set file name for saving time point of first pullup
    base.pullupTimeFirstFileName = 'pullupTimeFirst.txt'
    # Set file path
    base.pullupTimeFirstFilePath = os.path.join(base.scriptPath, 'data', base.pullupTimeFirstFileName)
    # Set file name for saving time point of last pullup
    base.pullupTimeLastFileName = 'pullupTimeLast.txt'
    # Set file path
    base.pullupTimeLastFilePath = os.path.join(base.scriptPath, 'data', base.pullupTimeLastFileName)

    # Set file path for saving pullup counts
    # This folder path is mounted through the docker run command also
    base.pullupCountsFilePath = os.path.join(base.scriptPath, 'data', base.pullupCountsFileName) 
    # Set folder name for saving stream
    base.streamSaveFolderName = 'pullupSave'
    # Set name of video produced by YOLOv8n pose estimation
    base.streamSaveFileName = 'video.avi'
    # Set file path for saving stream
    base.streamSaveFolderPath = os.path.join(base.scriptPath, 'data', base.streamSaveFolderName)
    

    ### Data configuration ###
    # Set operations file path
    data.operationModeFilePath = os.path.join(base.scriptPath, 'data', 'pullupSoundsOperation.txt')
    # Read the file with the operation mode status
    with open(data.operationModeFilePath, 'r') as f:
        # Read the status
        HAOperationMode = f.read()
        # Newline character included, use in
        if 'normal' in HAOperationMode:
            data.operationMode = 'normal'
        if 'simulate' in HAOperationMode: # Simulate mode
            data.operationMode = 'simulate'

    # Get OS type so we can use it both on linux server without display and windows workstation with display
    base.osType = os.name
    # If OS is Linux disable some features and set some parameters
    if (base.osType == 'posix'):
        data.showStream = False
        data.playSound = False
        data.playSonos = True
        data.saveStream = True
        data.videoSource = 'stream' # Pullup stream from file 'streamWithPassword.url
        data.saveTxt = True # Save txt file with pose estimation results
        data.saveConf = True # Save confidence information in txt file
    else: 
        data.showStream = True
        data.playSound = True
        data.playSonos = True
        data.saveStream = True
        data.videoSource = '0' # Webcam
        data.saveTxt = False # Save txt file with pose estimation results
        data.saveConf = False # Save confidence information in txt file

    # Set threshold for relative height of bar with respect to image height
    # Image coordinates is starting in upper left corner. Detected point used in the model is nose. 
    # This is really hard due to paralax error.
    #data.barRelativeHight = 0.5 # Due to paralax error, this cannot be used as RX standard. 
    #data.barRelativeHight = 0.38 # This is mouth over bar. Choose this and have some wiggle room for paralax erros.
    #data.barRelativeHight = 0.29 # This is chin over over bar. 
    data.barRelativeHight = 0.35 # Ratio for bar in the image, bar a bit raised (camera pointing down). 

    # Set needed confidence for a pullup to be counted
    data.noseConfidenceThreshold = 0.5 
    # Max video file size in bytes (1000 MB)
    data.maxVideoFileSize = 1000000000
    # Select YOLO model (nano or full)
    data.yoloModel = 'n' # n=nano, s=small, m=medium, l=large, x=full 
    # Set theme for sound chime (not Sonos)
    data.soundTheme = 'mario'

    ### SONOS configuration ###
    # SONOS room to play sound in
    sonos.HASoundRoomFilePath = os.path.join(base.scriptPath, 'data', 'pullupSoundsSpeaker.txt')  
    # SONOS volume file
    sonos.HASoundVolumeFilePath = os.path.join(base.scriptPath, 'data', 'pullupSoundsVolume.txt')    
    # Set default local location for sound files
    sonos.soundBasePath = os.path.join(base.scriptPath, 'sounds', 'military')
    # Set directory for sound files on webserver
    sonos.soundBasePathWeb = 'http://192.168.1.2/sounds'
    # Set file path for sound status
    sonos.HASoundStatusFilePath = os.path.join(base.scriptPath, 'data', 'pullupSounds.txt') # Determined in HA config
    # Set file path for sound theme
    sonos.HASoundThemeFilePath = os.path.join(base.scriptPath, 'data', 'pullupSoundsTheme.txt') # Determined in HA config
