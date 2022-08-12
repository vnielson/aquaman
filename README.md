# Aquaman Irrigation Project

## Overview
I had been interested in doing something with a Raspberry Pi for some time and after retirement I was going to start a 
vegetable garden and thought that a R Pi controlled irrigation system would be cool. So this project was born. 
I wanted to monitor soil moisture so the garden would watered at optimal times (not over-watered or under-watered).


## Development Technologies
This 
## Hardware Components Used


## Getting Started


## Runtime Configuration
The program is set up to run automatically via SYSTEMD configuration. 
Configuration setup is based on instruction found [HERE](https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/#:~:text=d%20directory,shutdown%20or%20reboot%20the%20system). See description of method 4.

### Service File
This is my service file defined in /lib/systemd/system/

    [Unit]
    Description=Aquaman
    After=multi-user.target

    [Service]
    User=pi
    WorkingDirectory=/home/pi/projects/aquaman
    Type=idle
    ExecStart=/usr/bin/python -u /home/pi/projects/aquaman/aquaman.py
    StandardOutput=file:/home/pi/projects/aquaman/aq.log
    StandardError=inherit
    User=pi

    [Install]
    WantedBy=multi-user.target

### Service Tasks (Starting, Stopping and Check status)
#### Check Status 
    sudo systemctl status aquaman.service
#### Start Service
    sudo systemctl start aquaman.service
#### Stop Service
    sudo systemctl stop aquaman.service
#### Check Service Logs
    sudo journalctl -f -u aquaman.service

####Aliases for Service 
alias starta='sudo systemctl start aquaman'
alias stata='sudo systemctl status  aquaman'
alias stopa='sudo systemctl stop aquaman'


## Aquaman Monitor
### Crontab entry

##Database
sqlite
can use sqlitebrowser on RPi

** Bold? **
asdfsd