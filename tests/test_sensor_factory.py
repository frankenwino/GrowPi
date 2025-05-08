import pytest
from growpi.sensors.sensor_factory import create_sensor, SENSOR_CLASSES


def test_create_sensor_valid_types():
    # Test for each valid sensor type
    for sensor_type, sensor_class in SENSOR_CLASSES.items():
        sensor = create_sensor(sensor_type, pin=20, name="TestSensor")
        assert isinstance(sensor, sensor_class)


def test_create_sensor_invalid_type():
    # Test for an invalid sensor type
    with pytest.raises(ValueError, match="Invalid sensor type: INVALID_SENSOR"):
        create_sensor("INVALID_SENSOR")


def test_create_sensor_missing_arguments():
    # Test for missing required arguments
    with pytest.raises(TypeError):
        create_sensor("AM2301")  # Missing 'pin' and 'name'
    with pytest.raises(TypeError):
        create_sensor("DS18B20", pin=4)
    with pytest.raises(TypeError):
        create_sensor("LM393", pin=5, name="TestSensor", extra_arg="extra")
    with pytest.raises(TypeError):
        create_sensor("AM2302", pin=23, name="TestSensor", extra_arg="extra")
