# import time
# import board
# import adafruit_dht
# import RPi.GPIO as GPIO
# import atexit
# from sensors.sensor_interface import SensorInterface
# from utils.now import get_utc_datetime

# class AM2301(SensorInterface):
#     """
#     AM2301 Temperature and Humidity Sensor.

#     Attributes:
#         pin (int): The BCM GPIO pin number the sensor is connected to.
#     """

#     def __init__(self, pin, name):
#         """
#         Initializes the AM2301 sensor.

#         Parameters:
#             pin (int): The GPIO pin number.
#             name (str): Name or identifier for the sensor.
#         """
#         GPIO.setmode(GPIO.BCM)
#         self.pin = pin
#         self.name = name

#         # Create sensor using board pin mapping
#         try:
#             gpio_attr = f"D{pin}"
#             board_pin = getattr(board, gpio_attr)
#             self.sensor = adafruit_dht.DHT22(board_pin, use_pulseio=False)
#         except AttributeError:
#             raise ValueError(f"Pin D{pin} not found on board module.")

#         # Ensure GPIO cleanup on exit
#         atexit.register(GPIO.cleanup)

#     def read_data(self):
#         """
#         Reads temperature and humidity data from the sensor.

#         Returns:
#             dict or None: A dictionary containing sensor readings, or None on failure.
#         """
#         try:
#             temperature = self.sensor.temperature
#             humidity = self.sensor.humidity

#             if temperature is None or humidity is None:
#                 raise RuntimeError("Received None from sensor")

#             return {
#                 "sensor": self.name,
#                 "temperature": round(temperature, 2),
#                 "humidity": round(humidity, 2),
#                 "date_time_utc": get_utc_datetime(),
#             }

#         except RuntimeError as e:
#             print(f"[{self.name}] Error reading sensor: {e}")
#             return None


# if __name__ == "__main__":
#     sensor = AM2301(20, "AM2301")
#     while True:
#         data = sensor.read_data()
#         if data:
#             print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")
#         else:
#             print("Sensor read failed. Retrying...")
#         time.sleep(2)

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

    def __init__(self, pin, name):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        self.name = name

        # Try mapping pin to board.DXX
        try:
            gpio_attr = f"D{pin}"
            board_pin = getattr(board, gpio_attr)
            self.sensor = adafruit_dht.DHT21(board_pin)
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
            print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")
        else:
            print("Sensor read failed. Retrying...")
        time.sleep(2)


# import time
# import board
# import adafruit_dht

# # Initial the dht device, with data pin connected to:
# dhtDevice = adafruit_dht.DHT21(board.D20)

# # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# # This may be necessary on a Linux single board computer like the Raspberry Pi,
# # but it will not work in CircuitPython.
# # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

# while True:
#     try:
#         # Print the values to the serial port
#         temperature_c = dhtDevice.temperature
#         temperature_f = temperature_c * (9 / 5) + 32
#         humidity = dhtDevice.humidity
#         print(
#             "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
#                 temperature_f, temperature_c, humidity
#             )
#         )

#     except RuntimeError as error:
#         # Errors happen fairly often, DHT's are hard to read, just keep going
#         print(error.args[0])
#         time.sleep(2.0)
#         continue
#     except Exception as error:
#         dhtDevice.exit()
#         raise error

#     time.sleep(2.0)
