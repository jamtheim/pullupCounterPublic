# Note: reference of public in pullupcounterpublic is just meaning the code is public uploaded to GitHub.
# Can be changed to whatever. 

# Stop and force-remove the container
docker rm -f pullupcounterpublic
# Build docker
t=pullupcounterpublic:latest && sudo docker build -f custom_Dockerfile-cpu_pullupcounter -t $t .

# Run in like this: (--net=host needed for network access)
# The docker can then be started and stopped through HA and the mount will persist. 
# docker run --net=host -v /home/automation/Automation/HomeAssistant/config/www:/usr/src/app/data --name pullupcounter  pullupcounter:latest 
# It can now be controlled with HA (=Home Assistant). 
# Adapted for public release
docker run --net=host -v ./data:/usr/src/app/data --name pullupcounterpublic  pullupcounterpublic:latest 
 
