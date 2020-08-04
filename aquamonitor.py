import psutil
import os
import datetime
from project.system_operation.emailer import Emailer
from project.sensors.views import get_sensors, get_sensor_reading
from project.sensors import moisturemeter


def aquaman_is_running():
    aquaman_running = False
    for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline']):
        cmdline = proc.info["cmdline"]
        full_command_line = ' '.join(str(i) for i in cmdline)
        if full_command_line.find("/aquaman.py") != -1:
            # print(full_command_line + str(proc.info["pid"]))
            aquaman_running = True

    return aquaman_running

def restart_aquaman():
    print("Restart Aquaman")
    os.system("sudo systemctl start aquaman")

# Function to check that the sensors are online and returning data
def check_sensors():
    all_sensors = get_sensors()

    for next_sensor in all_sensors:
        sensor_reading_data = get_sensor_reading(next_sensor.sensor_id)
        if (not sensor_reading_data["data_valid"]):
            print("Aquamonitor Sensor Check Failure:")
            print(sensor_reading_data)
            print(next_sensor.__dict__)


def check_sensor_readings():
    print("TODO: Add check for recent readings from all sensors")


def main():
    date_time = datetime.datetime.now()
    print("=========== AQUAMAN MONITOR BEGIN  ===========")
    print(date_time)

    check_sensors()

    check_sensor_readings()

    if (not aquaman_is_running()):
        print("Aquaman not found!!!!")
        restart_aquaman()



    # sender = Emailer()
    #
    # sendTo = 'vnielson18@gmail.com'
    # emailSubject = "Hello World"
    # emailContent = "This is a test of my Emailer Class"
    #
    # # Sends an email to the "sendTo" address with the specified "emailSubject" as the subject and "emailContent" as the email content.
    # sender.sendmail(sendTo, emailSubject, emailContent)
    #

    print("=========== END OF RUN ===========")



if __name__ == '__main__':
    main()

