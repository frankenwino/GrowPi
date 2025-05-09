import pytest
from growpi.sensors.sensor_factory import create_sensor, SENSOR_CLASSES


def test_create_sensor_valid_types():
    # Arrange
    for sensor_type, sensor_class in SENSOR_CLASSES.items():
        # Act
        sensor = create_sensor(sensor_type, pin=20, name="TestSensor")
        # Assert
        assert isinstance(sensor, sensor_class)


def test_create_sensor_invalid_type():
    # Arrange & Act
    with pytest.raises(ValueError, match="Invalid sensor type: INVALID_SENSOR"):
        create_sensor("INVALID_SENSOR")  # Act


def test_create_sensor_missing_arguments():
    # Arrange & Act
    with pytest.raises(TypeError):
        create_sensor("AM2301")  # Act
    with pytest.raises(TypeError):
        create_sensor("DS18B20", pin=4)  # Act
    with pytest.raises(TypeError):
        create_sensor("LM393", pin=5, name="TestSensor", extra_arg="extra")  # Act
    with pytest.raises(TypeError):
        create_sensor("AM2302", pin=23, name="TestSensor", extra_arg="extra")  # Act
