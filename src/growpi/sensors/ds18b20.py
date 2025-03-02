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
        base_dir = "/sys/bus/w1/devices/"
        device_folder = glob.glob(base_dir + "28*")[0]  # Find sensor directory
        self.device_file = device_folder + "/w1_slave"
        self.pin = pin
        self.name = name

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
        lines = self._read_raw_data()
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self._read_raw_data()

        temp_output = lines[1].split("t=")[-1]
        if temp_output:
            return {
                "temperature": round(float(temp_output) / 1000.0, 1),
                "sensor": self.name,
                "date_time": get_utc_datetime()
            }
        return None

# if __name__ == "__main__":
#     sensor = DS18B20()
#     while True:
#         temperature = sensor.read_data()
#         print(f"Temperature: {temperature}°C")
#         time.sleep(2)
