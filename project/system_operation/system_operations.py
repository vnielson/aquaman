
from project.valves import views as valves
from project.sensors import views as sensors
from apscheduler.schedulers.background import BackgroundScheduler
import datetime

aqua_sched = BackgroundScheduler(daemon=True)


def initialize_scheduler():
    # aqua_sched.add_job(do_moister_readings, 'interval', seconds=30)
    aqua_sched.add_job(do_moister_readings, 'interval', minutes=10)
    aqua_sched.add_job(func=do_watering, args=[False], trigger='interval', minutes=20)
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


def crop_needs_watering(crop, kpa, test_mode):
    print("In crop needs watering:")
    print("Crop Dry KPA: " + str(crop.dry_kpa))
    print("Current  KPA: " + str(kpa))
    # if the current kpa is above the crop 'dry' kpa, then watering is needed
    watering_needed = False
    if (kpa > crop.dry_kpa):
        print("Crop is too dry, needs watering")
        watering_needed = True

    if (test_mode):
        watering_needed = True

    # return watering_needed
    return watering_needed


def water_crop(crop, valve_id, trigger_kpa):
    print("In water crop")
    print(crop.__dict__)
    print("Valve " + str(valve_id))
    open_status = valves.open_valve(valve_id, True, trigger_kpa)
    print("Open status returned")
    print(open_status)
    close_valve_date_time = datetime.datetime.now() + datetime.timedelta(minutes = 2)
    # aqua_sched.add_date_job(func=valves.close_valve, args=valve_id, date=close_valve_date_time)
    aqua_sched.add_job(func=valves.close_valve,
                       args=[valve_id,True,open_status["event_id"]], trigger='date',
                       run_date=close_valve_date_time)


def in_watering_window():
    # function to see if current time is within watering window or not
    # that is, is it ok to water or not
    watering_hour_min = 8
    watering_hour_max = 18

    print("In check watering window")
    time_now = datetime.datetime.now()
    hour_now = time_now.hour

    # ret_val = False
    if ((hour_now >= watering_hour_min) and (hour_now <= watering_hour_max)):
        print("In watering window")
        in_window = True
    else:
        print("NOT In watering window")
        in_window = False

    print("Time now hour is: ")
    print(time_now.hour)

    #Simple first version, returns true always
    return in_window


#     Checks each sensor moisture values and waters
#     if needed.
def do_watering(test_mode):
    print("====================================")
    print("SYSOPS: Do Watering ...")
    print(test_mode)
    print("====================================")

    if (in_watering_window() or test_mode):
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
            if (crop_needs_watering(crop, avg_kpa, test_mode)):
                water_crop(crop, nxt_sensor.valve_id, avg_kpa)

