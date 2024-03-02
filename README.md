# Pullup Counter

Video analytics based pullup counter written in Python and run in a docker container. It analyzes a video stream from a network camera of the athlete doing pullups using the Ultralytics YOLOv8 pose estimation deep learning model. Specifically it compares the position of the athlete nose point towards the position of the bar in the image. This solution is adapted to run on a CPU, and does not require a GPU. 
This code provides a working Python environment but does not include code adaptations to Home Assistant integrations. I realize this code will require some adaptions to your local network environment but hope it will provide you with some inspiration for future projects. If needed, contact mee through LinkedIn.

## Table of Contents

- [Features](#features)  
- [Installation](#installation)  
- [Usage and limitations](#usage)
- [Demo](#demo)

## Features  
- Counts your pullups and saves the result in a text file.  
- Integration with Home Assistant is prepared. 
- Can play sound through any SONOS speaker on the same network upon a successful pullup. How about some sounds from Full Metal Jacket? (not shared due to copyright)

## Installation  
1. Edit the `streamWithPassword.url` file with the following contents to user setting:  
   `http://user:pass@ipAddressOfCamera/videoFilePath`  
2. Set up your camera so the pullup bar is in the middle of the height of the image. 
3. Adapt `commonConfig.py` for local folders.
4. If you want sounds for SONOS, make sure to include sounds folder when building the docker. Also 
make sure the corresponding folder exist on a local webserver. See commonConfig.py. 
Special sounds are included for every 5 pullup up to 55 :) 
5. Run `buildMyContainerAndRun.sh`. 
6. Code for Home Assistant configuration is not provided. Can be shared upon request though. Basically Home Assistant reads and writes txt files for setting and controlling config of pullupcounter. 

## Usage and limitations
- See `buildMyContainerAndRun.sh` for the docker run command.  
- Configuration might need adaptation for mounting selected folders. 
- The pretrained nano YOLOv8n pose model has an inference time of about 100 ms on a CPU with 4 cores for a i5-6200U CPU (released in 2015) @ 2.30GHz using 480x640 resolution. 
- Model performance is limited in dark lightning conditions. Ultralytics YOLO allows for model retraining though. 
- Be aware of parallax phenomena depending on the angle of the camera and the pullup bar. See setting in commonConfig.py for defining the image height threshold. 

## Demo  
- Sorry for video being out of sync for left and right. It was challenging to sync both with variable frame rate from the right one. 

https://github.com/jamtheim/pullupCounterPublic/assets/46457468/bdb78075-1f39-453b-b565-0bc53173c0ef


![HomeAssistantScreen](https://github.com/jamtheim/pullupCounterPublic/assets/46457468/7fc7e76e-c9b3-4ea4-840b-2f82e943a6f8)





