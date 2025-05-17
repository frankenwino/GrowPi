# import RPi.GPIO as GPIO
# import atexit
from utils.now import get_utc_datetime
from sensors.sensor_interface import SensorInterface
import random

class PHDummy(SensorInterface):
    """
    PhDummy Sensor Class.

    """

    def __init__(self, pin, name):
        """Initialize sensor with the GPIO pin number."""
        self.pin = pin
        self.name = name
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.pin, GPIO.IN)

        # # Cleanup GPIO at exit
        # atexit.register(GPIO.cleanup)

    def read_data(self):
        """
        Reads light intensity data from the sensor.

        Returns:
            dict: A dictionary containing CO2 PPM and timestamp.
        """
        # sensor_value = GPIO.input(self.pin)
        sensor_value = round(random.uniform(5.0, 8.5), 1)
        return {
            "sensor": self.name,
            "ph": sensor_value,
            "reading_timestamp_utc": get_utc_datetime(),
        }

    # def light_detected(self, sensor_readout):
    #     """Determine if it's dark or light based on the sensor readout."""
    #     return sensor_readout == 0  # True if light is detected


if __name__ == "__main__":
    from pprint import pprint


    pin = 21  # physical pin 40
    sensor = PHDummy(pin, "PHDummy")

    pprint(sensor.read_data())
