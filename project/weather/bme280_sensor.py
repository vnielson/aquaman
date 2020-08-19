import smbus2
import bme280
from project.core.aqualogger import weatherlog


class bme280_sensor:

    def __init__(self):
        self.port = 1
        self.address = 0x77
        self.bus = smbus2.SMBus(self.port)

    def convert_raw_reading_to_us_units(self, raw_data):
        converted_data = {}
        converted_data["id"] = raw_data.id
        converted_data["timestamp"] = raw_data.timestamp
        # T(°F) = T(°C) × 9 / 5 + 32

        converted_data["temp"] = (raw_data.temperature*9/5) + 32
        # pinHg = 0.02952998751 × phPa

        converted_data["pressure"] = raw_data.pressure*0.02952998751
        converted_data["humidity"] = raw_data.humidity

        return converted_data

        # compensated_reading(id=b556763a-fd27-4fa1-a5ee-3547be3d6f04, timestamp=2020-08-14 12:57:06.675306, temp=29.064 °C, pressure=926.84 hPa, humidity=18.53 % rH)


    def get_weather_reading(self):
        calibration_params = bme280.load_calibration_params(self.bus, self.address)

        # the sample method will take a single reading and return a
        # compensated_reading object
        raw_data = bme280.sample(self.bus, self.address, calibration_params)

        weatherlog.info("Raw data type : %s", raw_data)

        # # the compensated_reading class has the following attributes
        # print(data.id)
        # print(data.timestamp)
        # print(data.temperature)
        # print(data.pressure)
        # print(data.humidity)

        # there is a handy string representation too
        weatherlog.info("Raw Weather Reading:")
        weatherlog.info(raw_data)

        converted_data = self.convert_raw_reading_to_us_units(raw_data)

        return converted_data

