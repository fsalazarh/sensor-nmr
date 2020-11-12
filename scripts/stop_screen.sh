#!/bin/bash

# Controller

if screen -list | grep -q "controller"; then
    echo "\033[0;32m STOPPING SCREEN CONTROLLER  \033[0m "
    screen -S controller -p 0 -X stuff $'\003'
    sleep 0.5
    screen -S controller -p 0 -X stuff $'\003'
    screen -S controller -p 0 -X stuff "`printf "exit \r"`"
    sleep 0.5
else
    echo "\033[0;31m SCREEN CONTROLLER IS NOT RUNNING \033[0;0m"
fi
