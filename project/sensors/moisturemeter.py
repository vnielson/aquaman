import RPi.GPIO as GPIO  # import RPi.GPIO module
from datetime import datetime
import numpy as np


class MoistureMeter:
    def __init__(self, id, bcmpin):
        self.id = id
        self.bcmpin = int(bcmpin)
        # set up the pin for input
        print("GPIO BCM Value is : ", GPIO.BCM)
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setup(self.bcmpin, GPIO.IN)  # set input pin as an
        print("GPIO Pin " + str(self.bcmpin) + " set as input")

    def __str__(self):
        ret_string = "ID: {id}  BCM PIN: str(bcmpin)".format(id=self.id, bcmpin=self.bcmpin)
        return ret_string

    def compute_kpa(self, frequency):
        # function to calculate the kPA value based on the input frequency.

        print("compute_kpa input frequency is : ", frequency)

        if frequency > 6430:
            kPa = 0
        elif frequency > 4330 and frequency <= 6430:
            kPa = 9 - ((frequency - 4600) * 0.004286)
        elif frequency > 2820 and frequency <= 4330:
            kPa = 15 - ((frequency - 2820) * 0.00291)
        elif frequency > 1110 and frequency <= 2820:
            kPa = 35 - ((frequency - 1110) * 0.01170)
        elif frequency > 770 and frequency <= 1110:
            kPa = 55 - ((frequency - 770) * 0.05884)
        elif frequency > 600 and frequency <= 770:
            kPa = 75 - ((frequency - 600) * 0.1176)
        elif frequency > 485 and frequency <= 600:
            kPa = 100 - ((frequency - 485) * 0.2174)
        elif frequency > 293 and frequency <= 485:
            kPa = 200 - ((frequency - 293) * 0.5208)
        elif frequency <= 293:
            kPa = 200

        return int(kPa)

    def get_kpa_value(self):
        # set up the pin for input
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        GPIO.setup(self.bcmpin, GPIO.IN)  # set input pin as an
        print("GPIO Pin " + str(self.bcmpin) + " set as input")
        # Set up callback for sensor input (rising edge)

        print("Begin gathering sensor data for sensor " + str(self.id) + "  " + str(self.bcmpin))

        print("self.bcmpin is ", self.bcmpin)
        state = GPIO.input(self.bcmpin)
        print("State is ", state)
        # wait for first rising edge detection

        # wait for up to 5 seconds for a rising edge (timeout is in milliseconds)
        channel = GPIO.wait_for_edge(self.bcmpin, GPIO.RISING, timeout=5000)

        if channel is None:
            print('Timeout occurred')
        else:
            print('Edge detected on channel', channel)

        # start timer to begin measuring

        tstart = datetime.now()
        # print("Time Start : ", tstart)

        # sample_count = 500
        sample_count = 25

        per_array = np.zeros(sample_count)

        valid_data = True

        # now loop, repeatedly looking for rising edge and timing info
        for i in range(0, sample_count):
            channel = GPIO.wait_for_edge(self.bcmpin, GPIO.RISING, timeout=5000)

            if channel is None:
                print('Timeout occurred, abort')
                kPa = -1
                valid_data = False
                break
            else:
                tend = datetime.now()
                time_delta = tend - tstart
                # print("Delta for this loop: ",time_delta.total_seconds())
                per_array[i] = time_delta.total_seconds()
                tstart = datetime.now()

            channel = GPIO.wait_for_edge(self.bcmpin, GPIO.FALLING, timeout=5000)

        # for x in range(0, sample_count):
        #     print("per_array: " + str(x) + "  ", 1/per_array[i])

        if (valid_data):
            # Calculate final kPa data
            total_time_measured = per_array.sum()

            period = total_time_measured / sample_count
            frequency = 1 / period

            # print("calculated period : ", period)
            kPa = self.compute_kpa(frequency)

            # compute some statistics that might help understand how well the system is working
            min_frequency = 1.0 / per_array.max()
            max_frequency = 1.0 / per_array.min()
            mean = 1 / per_array.mean()
            stddev = per_array.std()

        return_data = {"kpa_value": kPa, "computed_frequency": frequency, "min_frequency": min_frequency,
                       "max_frequency": max_frequency, "mean": mean, "std_dev": stddev}



        return return_data
