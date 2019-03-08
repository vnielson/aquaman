from project import db
from project.sensors import moisturemeter
from project.models import Sensor_Info
from project.models import SensorReadings
import RPi.GPIO as GPIO  # import RPi.GPIO module

def main():
    print("main program for moisture reading")
    sensors = Sensor_Info.query.all()

    #    print("By Row:")
    #    for row in sensorinfo:
    #        print("Row:", row)

    for sensor_data in sensors:
        print("Next Sensor: {} {} {}".format(sensor_data.sensor_id, sensor_data.crop, sensor_data.bcm_pin))
        nxt_sensor = moisturemeter.MoistureMeter(sensor_data.sensor_id, sensor_data.bcm_pin)
        print("get kPa for : ", sensor_data.sensor_id)
        sensor_reading_data = nxt_sensor.get_kpa_value()
        print("Return data: ", sensor_reading_data)

        new_reading = SensorReadings(sensor_data.sensor_id, sensor_reading_data)
        db.session.add(new_reading)
        db.session.commit()


    print("=========== END OF RUN ===========")

    # Clean up GPIO
    GPIO.cleanup()


if __name__ == '__main__':
    main()