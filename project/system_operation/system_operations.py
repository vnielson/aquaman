
from project.valves import views as valves
from project.sensors import views as sensors
from apscheduler.schedulers.background import BackgroundScheduler

import datetime

aqua_sched = BackgroundScheduler(daemon=True)


def initialize_scheduler():
    aqua_sched.add_job(do_moister_readings, 'interval', minutes=5)
    aqua_sched.start()


def initialize_system():
    print("In system Initialization")

    all_valves = valves.close_all_valves()
    print("All Valves")
    print(all_valves)


def do_moister_readings():
    print("====================================")
    print("SYSOPS: Do Moisture Readings...")
    print("====================================")
    sensors.do_sensor_readings()


def get_average_kpa(sensor_readings):
    print("In get average kpa")
    reading_count = 0
    total_kpa = 0
    for sr in sensor_readings:
        print("Next KPA: " + str(sr.kpa_value))
        total_kpa += sr.kpa_value
        reading_count += 1

    avg_kpa = total_kpa/reading_count
    print("Computed average KPA is : " + str(avg_kpa))

    return avg_kpa


def crop_needs_watering(crop, kpa):
    print("In crop needs watering:")
    print("Crop Dry KPA: " + str(crop.dry_kpa))
    print("Current  KPA: " + str(kpa))
    # if the current kpa is above the crop 'dry' kpa, then watering is needed
    watering_needed = False
    if (kpa > crop.dry_kpa):
        watering_needed = True

    # return watering_needed
    return True

def water_crop(crop, valve_id, trigger_kpa):
    print("In water crop")
    print(crop.__dict__)
    print("Valve " + str(valve_id))
    open_status = valves.open_valve(valve_id, True, trigger_kpa)
    print("Open status returned")
    print(open_status)
    close_valve_date_time = datetime.datetime.now() + datetime.timedelta(minutes = 1)
    # aqua_sched.add_date_job(func=valves.close_valve, args=valve_id, date=close_valve_date_time)
    aqua_sched.add_job(func=valves.close_valve,
                       args=[valve_id,True,open_status["event_id"]], trigger='date',
                       run_date=close_valve_date_time)



#     Checks each sensor moisture values and waters
#     if needed.
def do_watering():
    print("====================================")
    print("SYSOPS: Do Watering ...")
    print("====================================")

    all_sensors = sensors.get_sensors()

    for nxt_sensor in all_sensors:
        print("Process sensor: " )
        print(nxt_sensor.__dict__)
        # Get latest readings and determine an average current KPa value
        readings = sensors.get_latest_sensor_readings(nxt_sensor.sensor_id, 5)
        print(readings)
        avg_kpa = get_average_kpa(readings)
        crop = nxt_sensor.crops
        print("Crop for sensor is:")
        print(crop.__dict__)
        if (crop_needs_watering(crop, avg_kpa)):
            water_crop(crop, nxt_sensor.valve_id, avg_kpa)

