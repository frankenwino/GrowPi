from growpi.sensors.sensor_interface import SensorInterface


class MockAM2301(SensorInterface):
    """
    Mock class for the AM2301 (DHT22) temperature and humidity sensor.

    This class provides a mock implementation of the AM2301/DHT22 sensor
    for testing purposes. The sensor measures both temperature and relative
    humidity.
    """

    def __init__(self, pin, name):
        self.pin = pin
        self.name = name

    def read_data(self):
        return {"temperature": 25.0, "humidity": 50.0}
