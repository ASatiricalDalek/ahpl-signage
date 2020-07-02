#!/bin/bash
app="event-screen"
docker kill ${app}
docker rm ${app}
