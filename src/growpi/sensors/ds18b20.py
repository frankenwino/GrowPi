import glob
import time
from sensors.sensor_interface import Sensor
from utils.now import get_utc_datetime


class DS18B20(Sensor):
    """
    DS18B20 Temperature Sensor Class.

    Reads temperature data from the 1-Wire interface on a Raspberry Pi.
    """

    def __init__(self, pin, name):
        """Initialize sensor by finding the device file."""
        self.pin = pin
        self.name = name
        base_dir = "/sys/bus/w1/devices/"
        try:
            device_folder = glob.glob(base_dir + "28*")[0]
            self.device_file = device_folder + "/w1_slave"
        except IndexError:
            print(f"Warning: DS18B20 sensor not found at {base_dir}28*")
            self.device_file = None

    def _read_raw_data(self):
        """Reads raw temperature data from the sensor."""
        with open(self.device_file, "r") as f:
            return f.readlines()

    def read_data(self):
        """
        Reads and parses the temperature value.

        Returns:
            float: Temperature in Celsius.
        """
        if self.device_file is None:
            return {
                "sensor": self.name,
                "error": "Sensor not found",
                "date_time_utc": get_utc_datetime(),
            }

        lines = self._read_raw_data()

        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self._read_raw_data()

        temp_output = lines[1].split("t=")[-1]

        if temp_output:
            return {
                "sensor": self.name,
                "temperature": round(float(temp_output) / 1000.0, 1),
                "date_time": get_utc_datetime(),
            }
        return None


# if __name__ == "__main__":
#     sensor = DS18B20()
#     while True:
#         temperature = sensor.read_data()
#         print(f"Temperature: {temperature}°C")
#         time.sleep(2)
