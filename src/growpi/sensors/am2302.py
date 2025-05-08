import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import atexit
from sensors.sensor_interface import SensorInterface
from utils.now import get_utc_datetime

class AM2302(SensorInterface):
    """
    AM2302 Temperature and Humidity Sensor.

    Attributes:
        pin (int): The BCM GPIO pin number the sensor is connected to.
    """

    def __init__(self, pin, name):
        """
        Initializes the AM2301 sensor.

        Parameters:
            pin (int): The GPIO pin number.
            name (str): Name or identifier for the sensor.
        """
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.name = name

        # Create sensor using board pin mapping
        try:
            gpio_attr = f"D{pin}"
            board_pin = getattr(board, gpio_attr)
            self.sensor = adafruit_dht.DHT22(board_pin, use_pulseio=False)
        except AttributeError:
            raise ValueError(f"Pin D{pin} not found on board module.")

        # Ensure GPIO cleanup on exit
        atexit.register(GPIO.cleanup)

    def read_data(self):
        """
        Reads temperature and humidity data from the sensor.

        Returns:
            dict or None: A dictionary containing sensor readings, or None on failure.
        """
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity

            if temperature is None or humidity is None:
                raise RuntimeError("Received None from sensor")

            return {
                "sensor": self.name,
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "date_time_utc": get_utc_datetime(),
            }

        except RuntimeError as e:
            print(f"[{self.name}] Error reading sensor: {e}")
            return None


if __name__ == "__main__":
    sensor = AM2302(23, "AM2302")
    while True:
        data = sensor.read_data()
        if data:
            print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")
        else:
            print("Sensor read failed. Retrying...")
        time.sleep(2)
