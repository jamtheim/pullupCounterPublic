# *********************************************************************************
# Author: Christian Jamtheim Gustafsson, PhD, Medical Physcist Expert
# Description: 
# This script is used to count pullups from a video live stream using YOLOv8n pose estimation.
# We use the nose keypoint to determine if the athlete is above or below the bar.
# If the athlete is above the bar, we add to the pullup counter.
# We use chime to play a sound when a pullup is counted.
# We can also play a sound on a SONOS speaker when a pullup is counted.
# Information: 
# See https://docs.ultralytics.com/modes/predict/#keypoints
# https://alimustoofaa.medium.com/yolov8-pose-estimation-and-pose-keypoint-classification-using-neural-net-pytorch-98469b924525
# *********************************************************************************
from ultralytics import YOLO
import time 
import os 
import shutil
# Load modules
from commonConfig import commonConfigClass
from supportMethods import supportMethodsClass
# Init needed class instances
conf = commonConfigClass()          # Init config class
supportMethods = supportMethodsClass()       # Functions for reading an processing data 


### Init needed values ###
# Init the pullup counter
pullupCounts = 0
# Reset the time points for first pullup
pullupTimeFirst = 'Reset'
pullupTimeLast = 'Reset'
# Write time stamps to file
supportMethods.writeTimeStampFirstPullup(pullupTimeFirst)
supportMethods.writeTimeStampLastPullup(pullupTimeLast)
# Set initial flags for determining if athlete is going up or down with respect to bar
beenDown = False
beenUp = False


### Main ###
# Create file for storing pullup counts 
# Create new pullup count file if it does not exist
if not os.path.exists(conf.base.pullupCountsFilePath):
    with open(conf.base.pullupCountsFilePath, 'w') as f:
        f.write('0')
else:
    # Read logged pullup count from existing file
    with open(conf.base.pullupCountsFilePath, 'r') as f:
        pullupCounts = int(f.read())
        print('Pullup count from existing file is ' + str(pullupCounts))

# Check if video stream save folder exist
# It is created automatically by YOLOv8n pose estimation
# and should therefore be deleted before starting the script
if os.path.exists(conf.base.streamSaveFolderPath):
    print('Stream save folder existed as ' + conf.base.streamSaveFolderPath)
    # Remove it
    shutil.rmtree(conf.base.streamSaveFolderPath)
    print('Stream save folder was deleted')
    print(' ')
else: 
    print(conf.base.streamSaveFolderPath + ' does not exist')
    print('Will be created by YOLOv8n pose estimation later')
    print(' ')

# Determine video source
if (conf.data.videoSource == 'stream'):
    # Get pullup stream URL from file
    # Read from file streamWithPassword.url
    with open(os.path.join(conf.base.scriptPath,'streamWithPassword.url')) as f:
        source = f.read()
else:
    source = '0'

# Load a pretrained YOLOv8n pose model (n=nano version, around 100 ms inference time on CPU with 4 cores for a i5-6200U CPU @ 2.30GHz, 480x640 image)
model = YOLO('yolov8' + conf.data.yoloModel + '-pose.pt')
# Run inference on the source
results = model(source, stream=True, show=conf.data.showStream, save=conf.data.saveStream, device="CPU", show_labels=True, show_conf=True, show_boxes=True, project=os.path.join(conf.base.scriptPath, 'data'), name=conf.base.streamSaveFolderName, save_conf=conf.data.saveConf, save_txt=conf.data.saveTxt) #generator of Results objects

# Check if nose is above or below bar and add to pullup counter
for r in results:

    # For debugging and checking update interval
    if conf.data.operationMode == 'simulate':
        # Simulate a pullup every second
        time.sleep(2)
        pullupCounts, beenUp, beenDown = supportMethods.pullupCounterAdd(pullupCounts, True, True)

    # Video file for saving size should not be too big, make sure it is deleted with regular intervals.    
    supportMethods.deleteVideoWhenNeeded(os.path.join(conf.base.streamSaveFolderPath, conf.base.streamSaveFileName))

    # Main object detection block
    # Nose is object 0 in the COCO list of keypoints
    # Get the confidence of the nose and relative coordinates in the image
    # Wrap in try/except to avoid error when no keypoints are detected
    try: 
        noseConf = r.keypoints.conf[0][0].numpy()
        relCoord = r.keypoints.xyn[0][0].numpy()
        # Check if nose is detected (confidence above 0.5)
        if (noseConf > conf.data.noseConfidenceThreshold):
            # Check if pullup is above set relative threshold
            if (relCoord[1] >= conf.data.barRelativeHight):
                # Set flag
                beenDown = True    
            # If nose is above bar (coorinate starts at top left corner of image and goes down and right)
            if (relCoord[1] < conf.data.barRelativeHight):
                print('Relative coordinates of nose above bar is ' + str(relCoord[1]))
                beenUp = True            
                # Add to the pullup counter and reset flags back to False
                pullupCounts, beenUp, beenDown  = supportMethods.pullupCounterAdd(pullupCounts, beenUp, beenDown)

    except:
        pass    
