#!/bin/bash

# Variable called app used for naming
app="event-screen"
# Builds the docker container with the tag as the variable val. Must run from dir w/ Dockerfile
docker build -t ${app} .

# Runs the newly built container in daemon mode (-d) so it is in the background
# Maps container port 80 to host port 5000
# Sets the name of the running container to the app val for easy management
# Sets the present working directory as a volume within the contianer
# The last app variable call is to tell docker which image to run
docker run -d -p 5000:80 \
	--name=${app} \
	-v $PWD:/app ${app}

