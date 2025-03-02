import time
import board
import adafruit_dht
from sensors.sensor_interface import Sensor
from utils.now import get_utc_datetime


class AM2301(Sensor):
    """
    AM2301 Temperature and Humidity Sensor.

    Attributes:
        pin (int): The GPIO pin number the sensor is connected to.
    """

    def __init__(self, pin, name):
        """
        Initializes the AM2301 sensor.

        Parameters:
            pin (int): The GPIO pin number.
        """
        self.sensor = adafruit_dht.DHT22(getattr(board, f"D{pin}"), use_pulseio=False)
        self.pin = pin
        self.name = name

    # @staticmethod
    def read_data(self):
        """
        Reads temperature and humidity data from the sensor.

        Returns:
            dict: A dictionary containing temperature and humidity.
        """
        try:
            temperature = self.sensor.temperature
            humidity = self.sensor.humidity
            return {
                "sensor": self.name,
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2),
                "date_time_utc": get_utc_datetime(),
            }
        except RuntimeError as e:
            # return {
            #     "error": f"Error reading AM2301 sensor: {e}",
            #     "sensor": self.name,
            #     "date_time": get_utc_datetime()
            # }
            print(f"Error reading AM2301 sensor: {e}")
            return None


# if __name__ == "__main__":
#     sensor = AM2301()
#     while True:
#         data = sensor.read_data()
#         print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")
#         time.sleep(2)
