import RPi.GPIO as GPIO
import atexit
from utils.now import get_utc_datetime
from sensors.sensor_interface import SensorInterface


class LM393(SensorInterface):
    """
    LM393 Light Sensor Class.

    Reads light intensity data from a light-dependent resistor (LDR) connected to a GPIO pin.
    """

    def __init__(self, pin, name):
        """Initialize sensor with the GPIO pin number."""
        self.pin = pin
        self.name = name
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        # Cleanup GPIO at exit
        atexit.register(GPIO.cleanup)

    def read_data(self):
        """
        Reads light intensity data from the sensor.

        Returns:
            dict: A dictionary containing light intensity and timestamp.
        """
        sensor_value = GPIO.input(self.pin)
        return {
            "sensor": self.name,
            "light_detected": self.light_detected(sensor_value),
            "reading_timestamp_utc": get_utc_datetime(),
        }

    def light_detected(self, sensor_readout):
        """Determine if it's dark or light based on the sensor readout."""
        return sensor_readout == 0  # True if light is detected


if __name__ == "__main__":
    from pprint import pprint

    pin = 21  # physical pin 40
    sensor = LM393(pin, "LM393")

    pprint(sensor.read_data())
