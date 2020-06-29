from project import db
from project.sensors import moisturemeter
from project.models import Sensors
from project.models import SensorReadings
from project.models import Crops
from project.models import WateringEvent


import RPi.GPIO as GPIO  # import RPi.GPIO module

def do_moisture_sensor_readings():
    moisture_sensors = Sensors.query.all()

   # print("By Row:")
   # for row in sensorinfo:
   #     print("Row:", row)

    for moisture_sensor_data in moisture_sensors:
        print("Next Sensor: {} {} {}".format(moisture_sensor_data.sensor_id, moisture_sensor_data.crop, moisture_sensor_data.bcm_pin))
        nxt_sensor = moisturemeter.MoistureMeter(moisture_sensor_data.sensor_id, moisture_sensor_data.bcm_pin)
        print("get kPa for : ", moisture_sensor_data.sensor_id)
        sensor_reading_data = nxt_sensor.get_kpa_value()
        print("Return data: ", sensor_reading_data)

        new_reading = SensorReadings(moisture_sensor_data.sensor_id, sensor_reading_data)
        db.session.add(new_reading)
        db.session.commit()


def in_watering_window():
    # function to see if current time is within watering window or not
    # that is, is it ok to water or not
    print("In check watering window")
    #Simple first version, returns true always
    return True

def schedule_watering_events():
    # This function checks recent soil moisture readings against the sensors crop information and schedules
    # a watering event if needed
    print("In schedule_watering_events")
    moisture_sensors = Sensors.query.all()

    for moisture_sensor_data in moisture_sensors:
        print("Next Sensor: {} {} {}".format(moisture_sensor_data.sensor_id, moisture_sensor_data.crop, moisture_sensor_data.bcm_pin))
        #Get most recent sensor reading
        latest_reading = SensorReadings.query.order_by(SensorReadings.recorded_at.desc()).first()
        print("Latest Sensor Reading: recorded_at {} kpa {}".format(latest_reading.recorded_at,latest_reading.kpa_value))
        #Get Crop data associated with this sensor
        crop_data = Crops.query.get(moisture_sensor_data.crop)
        print("Associated crop info crop {} ideal_kpa {} dry_kpa {} sat_kpa {}".format(crop_data.crop, crop_data.ideal_kpa, crop_data.dry_kpa, crop_data.saturated_kpa))
        # See if we need to water. Is soil too dry
        if latest_reading.kpa_value > crop_data.dry_kpa:
            # Too dry, need to schedule watering event
            print("Schedule watering event for sensor {} dryKpa {}  Kpa Reading {} ".format(latest_reading.sensor_id, crop_data.dry_kpa, latest_reading.kpa_value))
            watering_event = WateringEvent(moisture_sensor_data.valve, 60*5, latest_reading.kpa_value)
            db.session.add(watering_event)
            db.session.commit()



def do_watering():
    # This function checks for new watering events and opens/closes appropriate valves as needed to water
    print("In do watering function")

    #get a watering event in the 'New' state, if there is such a thing. Get just the first one, since at this point
    # we only deal with one event at a time serially

    watering_event = WateringEvent.query.filter_by(state='new').first()

    if watering_event:
        print("Hello")
        #Determine open time

        #Create a valve object

        #Open the valve

        #Update watering event

        #Delay for the open 

def main():
    print("main program for checking soil moisture readings and watering if necessary")

    # check soil moisture readings and record data
    do_moisture_sensor_readings()


    #If we are in a watering window, then check the sensor data and schedule watering events

    if in_watering_window():
        schedule_watering_events()
        do_watering()




    print("=========== END OF RUN ===========")

    # Clean up GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    main()