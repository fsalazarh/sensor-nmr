#!/bin/bash
pad_path="/home/pi/sinestesia/noise"

# Noise controller

if ! screen -list | grep -q "controller"; then
    echo "\033[0;32m STARTING SCREEN CONTROLLER  \033[0m "
    sleep 0.5
    screen -dmS controller bash -c "exec bash"
    sleep 0.5
    screen -S controller -p 0 -X stuff "`printf "cd $pad_path \r"`"
    sleep 0.5
    screen -S controller -p 0 -X stuff "`printf "python3 controller.py \r"`"
else
    echo "\033[0;31m CONTROLLER SCREEN IS ALREADY RUNNING \033[0;0m"
fi
