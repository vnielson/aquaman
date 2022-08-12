
from project.valves import views as valves
from project.sensors import views as sensors
from project.weather import views as weather_sensors

from apscheduler.schedulers.background import BackgroundScheduler
from project.core.aqualogger import sysoplog, init_logging_system
from project.system_operation.emailer import Emailer


import datetime



aqua_sched = BackgroundScheduler(daemon=True)

def send_email_notice(subject, content):
    sender = Emailer()

    sendTo = 'vnielson18@gmail.com'
    # emailSubject = "Aquaman RESTART"
    # emailContent = "Aquaman was not found and so was restarted..."

    # Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
    sender.sendmail(sendTo, subject, content)


def initialize_system():
    init_logging_system("aquaman")

    # test_weather_device()

    # sysoplog.debug('This is a debug message')
    # sysoplog.info('This is an info message')
    # sysoplog.warning('This is a warning message')
    # sysoplog.error('This is an error message')
    # sysoplog.critical('This is a critical message')

    # sysoplog.basicConfig(filename=log_file_name, format='%(asctime)s: %(levelname) : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=sysoplog.DEBUG)
    sysoplog.info('Aquaman System Initialization')

    all_valves = valves.close_all_valves()
    sysoplog.info("All Valves")
    sysoplog.info(all_valves)


def initialize_scheduler():
    aqua_sched.add_job(do_moister_readings, 'interval', seconds=30)
    do_moister_readings_job =aqua_sched.add_job(do_moister_readings, 'interval', minutes=20)
    sysoplog.debug("Do moisture reading Job info:")
    sysoplog.debug(do_moister_readings_job.name)
    sysoplog.debug(do_moister_readings_job)
    # do_watering_job = aqua_sched.add_job(func=do_watering, args=[False], trigger='interval', minutes=60)
    # sysoplog.debug("Do Watering Job info:")
    # sysoplog.debug(do_watering_job.name)
    # sysoplog.debug(do_watering_job)
    # initial_water_check_date_time = datetime.datetime.now() + datetime.timedelta(minutes = 2)
    # # aqua_sched.add_date_job(func=valves.close_valve, args=valve_id, date=close_valve_date_time)
    # initial_water_check_job = aqua_sched.add_job(func=do_watering, args=[False],
    #                    trigger='date',
    #                    run_date=initial_water_check_date_time)
    # sysoplog.debug(initial_water_check_job.name)
    # sysoplog.debug(initial_water_check_job)

    do_weather_readings_job =aqua_sched.add_job(do_weather_readings, 'interval', minutes=15)
    # do_weather_readings_job =aqua_sched.add_job(do_weather_readings, 'interval', seconds=5)
    sysoplog.debug("Do weather reading Job info:")
    sysoplog.debug(do_weather_readings_job.name)
    sysoplog.debug(do_weather_readings_job)

    aqua_sched.start()



def do_weather_readings():
    sysoplog.info("====================================")
    sysoplog.info("SYSOPS: Do Weather Readings...")
    sysoplog.info("====================================")
    try:
        weather_sensors.do_weather_reading()
    except Exception:
        message = "Fatal error in do_weather_readings"
        send_email_notice("AQUAMAN: Exception Detected", message)
        sysoplog.exception(message)

def do_moister_readings():
    sysoplog.info("====================================")
    sysoplog.info("SYSOPS: Do Moisture Readings...")
    sysoplog.info("====================================")
    try:
        sensors.do_sensor_readings()
    except Exception:
        message = "Fatal error in do_moister_readings"
        send_email_notice("AQUAMAN: Exception Detected", message)
        sysoplog.exception(message)



def get_average_kpa(sensor_readings):
    sysoplog.debug("In get average kpa")
    reading_count = 0
    total_kpa = 0
    for sr in sensor_readings:
        # sysoplog.info("Next KPA: " + str(sr.kpa_value))
        total_kpa += sr.kpa_value
        reading_count += 1

    avg_kpa = total_kpa/reading_count
    sysoplog.debug("Computed average KPA is : " + str(avg_kpa))

    return avg_kpa


def crop_needs_watering(crop, kpa, test_mode):
    sysoplog.debug("In crop needs watering:")
    sysoplog.debug("Crop Dry KPA: " + str(crop.dry_kpa))
    sysoplog.debug("Current  KPA: " + str(kpa))
    # if the current kpa is above the crop 'dry' kpa, then watering is needed
    watering_needed = False
    if (kpa > crop.dry_kpa):
        sysoplog.info("Crop is too dry, needs watering: %s : Dry: %d Avg: %d", crop.crop_name, crop.dry_kpa, kpa)
        watering_needed = True

    if (test_mode):
        watering_needed = True

    # return watering_needed
    return watering_needed


def water_crop(crop, valve_id, trigger_kpa):
    sysoplog.info("In water crop")
    sysoplog.info(crop.__dict__)
    sysoplog.info("Valve " + str(valve_id))
    open_status = valves.open_valve(valve_id, True, trigger_kpa)
    sysoplog.info("Open status returned")
    sysoplog.info(open_status)
    close_valve_date_time = datetime.datetime.now() + datetime.timedelta(minutes = 8)
    # aqua_sched.add_date_job(func=valves.close_valve, args=valve_id, date=close_valve_date_time)
    end_watering_job = aqua_sched.add_job(func=valves.close_valve,
                       args=[valve_id,True,open_status["event_id"]], trigger='date',
                       run_date=close_valve_date_time)

    sysoplog.info("END Watering Job info:")
    sysoplog.info(close_valve_date_time)
    sysoplog.info(end_watering_job.name)
    sysoplog.info(end_watering_job)

    return end_watering_job



def in_watering_window():
    # function to see if current time is within watering window or not
    # that is, is it ok to water or not
    watering_hour_min = 8
    watering_hour_max = 18

    sysoplog.debug("In check watering window")
    time_now = datetime.datetime.now()
    hour_now = time_now.hour

    # ret_val = False
    if ((hour_now >= watering_hour_min) and (hour_now <= watering_hour_max)):
        sysoplog.debug("In watering window")
        in_window = True
    else:
        sysoplog.debug("NOT In watering window")
        in_window = False

    sysoplog.debug("Time now hour is: ")
    sysoplog.debug(time_now.hour)

    return in_window


#     Checks each sensor moisture values and waters
#     if needed.
def do_watering(test_mode):
    sysoplog.info("====================================")
    sysoplog.info("SYSOPS: Do Watering ...")
    sysoplog.debug(test_mode)
    sysoplog.info("====================================")
    try:
        watering_initiated = False

        if (in_watering_window() or test_mode):
            all_sensors = sensors.get_sensors()

            for nxt_sensor in all_sensors:
                sysoplog.debug("Process sensor: " )
                sysoplog.debug(nxt_sensor.__dict__)
                # Get latest readings and determine an average current KPa value
                readings = sensors.get_latest_sensor_readings(nxt_sensor.sensor_id, 3)
                sysoplog.debug(readings)
                avg_kpa = get_average_kpa(readings)
                sysoplog.debug(avg_kpa)
                crop = nxt_sensor.crops
                sysoplog.debug("Crop for sensor is:")
                sysoplog.debug(crop.__dict__)
                if (crop_needs_watering(crop, avg_kpa, test_mode)):
                    if (watering_initiated):
                        sysoplog.warning("Not watering due to watering in progress")
                    else:
                        water_job = water_crop(crop, nxt_sensor.valve_id, avg_kpa)
                        email_subject = "Watering Event Started"
                        email_content = 'Sensor:{sensor} Valve:{valve}   Crop:{crop} Expected End Time:{end}'.format(sensor=nxt_sensor.sensor_name,valve=nxt_sensor.valve_id,
                                                                                                     crop=crop.crop_name,
                                                                                                     end=water_job.trigger)
                        send_email_notice(email_subject, email_content)
                        watering_initiated = True
                else:
                    sysoplog.info("No crops need watering")
    except Exception:
        message = "Fatal error in do_watering"
        send_email_notice("AQUAMAN: Exception Detected", message)
        sysoplog.exception(message)



