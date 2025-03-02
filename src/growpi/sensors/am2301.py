import Adafruit_DHT
from sensors.sensor_interface import Sensor

class AM2301(Sensor):
    """
    Interface for the AM2303 (DHT22) temperature and humidity sensor.

    This class provides methods to interact with the AM2303/DHT22 sensor
    using the Adafruit_DHT library. The sensor measures both temperature
    and relative humidity.

    Parameters
    ----------
    pin : int
        The GPIO pin number where the sensor is connected.

    Attributes
    ----------
    _pin : int
        The GPIO pin number used by the sensor.
    sensor : Adafruit_DHT.AM2302
        The sensor type identifier.

    Examples
    --------
    >>> sensor = AM2303(pin=4)
    >>> data = sensor.read_data()
    >>> print(f"Temperature: {data['temperature']}°C, Humidity: {data['humidity']}%")

    Raises
    ------
    ValueError
        If the sensor data cannot be read successfully.
    """
    def __init__(self, pin):
        self._pin = pin
        self.sensor = Adafruit_DHT.AM2301
        
    def read_data(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self._pin)
        if humidity is None or temperature is None:
            raise ValueError('Failed to read data from sensor')
        
        return {
            'temperature': temperature,
            'humidity': humidity
        }