import time
import board
import adafruit_dht
import RPi.GPIO as GPIO
import atexit
from sensors.sensor_interface import SensorInterface
from utils.now import get_utc_datetime


class AM2301(SensorInterface):
    """
    AM2301 (DHT21) Temperature and Humidity Sensor.

    Attributes:
        pin (int): The BCM GPIO pin number the sensor is connected to.
        name (str): A human-readable identifier for the sensor.
    """

    def __init__(self, pin, name, sensor=None):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.name = name

        try:
            gpio_attr = f"D{pin}"
            board_pin = getattr(board, gpio_attr)
            # self.sensor = adafruit_dht.DHT21(board_pin)
            self.sensor = sensor or adafruit_dht.DHT21(board_pin)
        except AttributeError:
            raise ValueError(f"Pin D{pin} not found in board module.")

        # Ensure GPIO is cleaned up properly on exit
        atexit.register(GPIO.cleanup)

    def read_data(self):
        """
        Reads temperature and humidity from the AM2301 sensor.

        Returns:
            dict or None: Sensor data or None if reading fails.
        """
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity

            if temperature is None or humidity is None:
                raise RuntimeError("Sensor returned None values")

            return {
                "sensor": self.name,
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "date_time_utc": get_utc_datetime(),
            }

        except RuntimeError as e:
            print(f"[{self.name}] Sensor error: {e}")
            return None


if __name__ == "__main__":
    sensor = AM2301(20, "AM2301")  # Example: using GPIO 20
    while True:
        data = sensor.read_data()
        if data:
            print(
                f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%"
            )
        else:
            print("Sensor read failed. Retrying...")
        time.sleep(2)
