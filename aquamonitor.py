
import psutil
import os
import datetime
from project.core.aqualogger import monitorlog, init_logging_system

import time
from project.system_operation.emailer import Emailer
from project.sensors.views import get_sensors
from project.sensors import moisturemeter


def aquaman_is_running():
    aquaman_running = False
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
        cmdline = proc.info["cmdline"]
        full_command_line = ' '.join(str(i) for i in cmdline)
        if full_command_line.find("/aquaman.py") != -1:
            # monitorlog.debug(full_command_line + str(proc.info["pid"]))
            aquaman_running = True

    return aquaman_running

def restart_aquaman():
    monitorlog.info("Restart Aquaman")
    os.system("sudo systemctl start aquaman")

# Function to check that the sensors are online and returning data
# def check_sensors():
#     all_sensors = get_sensors()
#
#     for next_sensor in all_sensors:
#         # sensor_reading_data = get_sensor_reading(next_sensor.sensor_id)
#         if (not sensor_reading_data["data_valid"]):
#             monitorlog.debug("Aquamonitor Sensor Check Failure:")
#             monitorlog.debug(sensor_reading_data)
#             monitorlog.debug(next_sensor.__dict__)
#

def check_sensor_readings():
    monitorlog.debug("TODO: Add check for recent readings from all sensors")


def main():
    init_logging_system("monitor")

    date_time = datetime.datetime.now()
    monitorlog.info("=========== AQUAMAN MONITOR BEGIN  ===========")
    monitorlog.info(date_time)

    # monitorlog.debug("After Init... Wait 60 seconds")
    # time.sleep(60)

    # check_sensors()

    check_sensor_readings()

    # monitorlog.debug("After Sensor Check... Wait 60 seconds")
    # time.sleep(60)
    #
    if (not aquaman_is_running()):
        monitorlog.error("Aquaman not found!!!!")
        restart_aquaman()
        sender = Emailer()

        sendTo = os.getenv('MONITOR_EMAIL_SENDTO')
        print(f"Send EMAIL : {sendTo}")

        emailSubject = "Aquaman RESTART"
        emailContent = "Aquaman was not found and so was restarted..."

        # Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
        sender.sendmail(sendTo, emailSubject, emailContent)





    monitorlog.debug("=========== END OF RUN ===========")



if __name__ == '__main__':
    main()

