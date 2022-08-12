# Aquaman Irrigation Project

## Overview
I had been interested in doing something with a Raspberry Pi for some time and after retirement I was going to start a 
vegetable garden and thought that a R Pi controlled irrigation system would be cool. So this project was born. 
I wanted to monitor soil moisture so the garden would watered at optimal times (not over-watered or under-watered).

Although only a single code base, there are essentially three parts to the system. First is a web app that allows for 
system configuration, viewing and interacting with the system data. The second part of the application is the run-time
system that periodically checks sensors and determines if watering is needed. Lastly, a separate basic
system monitor programs checks that the service is running and restarts it if needed. 

The web app part: 
    1. Add any number of moisture sensors
    2. Add sprinkler valves
    3. Configure crop data and desired moisture ranges for the crop
    4. Mapping of moisture sensors to crops

At a high level the run-time system does the following:
    1. Initialize the sensors and relays
    2. Set the schedule for reading sensor data and checking for watering needs
    3. Read all moisture sensor data based on the prescribed schedule
    4. Periodically retreive the lastest sensor readings and compare to configured moisture reading ranges. If it is too dry, 
    a watering event is scheduled
    
As an afterthought, I added a basic temperature, humidity and pressure weather sensor and did some basic integration with the application.


## Development Technologies
* Python
* Flask
* SQLite

### Key Packages Used
* Numpy
* DyPlot
* APScheduler 
* smtplib (email)

Seven single-pole single throw relays
Rated at 120 volts AC or 30 volts DC

## Hardware Components Used

| Item | Description/Notes | Links |
|------|-------------------|------|
|Raspberry Pi 3 Model B|A less powerful model should work (Pi Zero W?)||
|Moisture Sensors | WATERMARK Soil Moisture Sensor| [Irrometer](https://www.irrometer.com/sensors.html#wm) |
|Soil Moister Interface| Converts Soil moisture sensor input for Rasperry pi|[EMESystems](https://emesystems.com/smx/main.html)|
|Pi-Plate Relay | Seven single-pole single throw relays </br> Rated at 120 volts AC or 30 volts DC| [Pi-Plate](https://pi-plates.com/relayr1/)|
|Enclosure| Bud Industries NBF-32018 Enclosure for housing the RPi, Relays etc |[BUD Industries](https://www.budind.com/product/nema-ip-rated-boxes/nbf-series-fiberglass-enclosure/nbf-32018/)|
|Terminal Block | Wire distribution block for sensors, valves, etc |[Amazon](https://www.amazon.com/Electronics-Salon-Position-Terminal-Distribution-Module/dp/B07BFXRBNY/) |
|DIN RAILS| Rails for mounting Terminal Block |[Amazon](https://www.amazon.com/gp/product/B079TX7WDQ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)|
|Weather Sensor | Waveshare BME280 Environmental Sensor, Temperature, Humidity, Barometric Pressure Detection Module I2C/SPI Interface for Weather Forecast, IoT Projects, ect |[Amazon](https://www.amazon.com/gp/product/B07P4CWGGK/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1) |
Note: The Watermark sensor and SMX interface can both be purchased together [HERE](https://emesystems.com/watermark/main.html)

These are just the specific components I chose to use. There are of course many options available.
I originally was looking at cheaper moisture sensors, but came to the conclusion that none of them
would last in an outdoor environment for very long. 

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
For the database, sqlite is used and sqlitebrowser is used as a db admin/monitor tool if/when needed
sqlite

