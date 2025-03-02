import RPi.GPIO as GPIO
from utils.now import get_utc_datetime

class LM393:
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

    def read_data(self):
        """
        Reads light intensity data from the sensor.
        
        Returns:
            dict: A dictionary containing light intensity and timestamp.
        """
        sensor_value = GPIO.input(self.pin)
        # self.cleanup()
        
        return {
            "light_detected": self.dark_or_light(sensor_value),
            "sensor": self.name,
            "date_time": get_utc_datetime()
        }

    def cleanup(self):
        """Cleans up the GPIO settings."""
        GPIO.cleanup()

    def dark_or_light(self, sensor_readout):
        """Determine if it's dark or light based on the sensor readout."""
        if sensor_readout == 0:
            return True  # Light detected
        else:
            return False  # Dark detected


# if __name__ == '__main__':
#     from pprint import pprint

#     # Create an instance of the LM393 class
#     pin = 37  # Physical pin number
#     sensor = LM393(pin, "LM393")

#     # Read data from the sensor
#     sensor_data = sensor.read_data()

#     # Determine if it is light or dark
#     result = sensor.dark_or_light(sensor_data["light_intensity"])

#     # Cleanup GPIO resources
#     sensor.cleanup()

#     # Print the result
#     pprint(result)
