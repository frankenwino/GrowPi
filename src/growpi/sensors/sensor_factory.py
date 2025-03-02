from sensors.am2301 import AM2301
from sensors.ds18b20 import DS18B20

SENSOR_CLASSES = {
    'AM2301': AM2301,
    'DS18B20': DS18B20
}

def create_sensor(sensor_type, **kwargs):
    sensor_class = SENSOR_CLASSES.get(sensor_type)
    if sensor_class is None:
        raise ValueError(f"Invalid sensor type: {sensor_type}")
    
    return sensor_class(**kwargs)