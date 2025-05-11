import pytest
from unittest.mock import patch, mock_open
from growpi.sensors.ds18b20 import DS18B20


@patch("growpi.sensors.ds18b20.glob.glob")
def test_sensor_initialization_found(mock_glob):
    # Arrange
    mock_glob.return_value = ["/sys/bus/w1/devices/28-0000065b1a2c"]

    # Act
    sensor = DS18B20(pin=4, name="TestSensor")

    # Assert
    assert sensor.device_file == "/sys/bus/w1/devices/28-0000065b1a2c/w1_slave"


@patch("growpi.sensors.ds18b20.glob.glob")
def test_sensor_initialization_not_found(mock_glob):
    # Arrange
    mock_glob.return_value = []

    # Act
    sensor = DS18B20(pin=4, name="TestSensor")

    # Assert
    assert sensor.device_file is None


@patch("builtins.open", new_callable=mock_open, read_data="YES\n t=21562")
@patch("growpi.sensors.ds18b20.glob.glob")
@patch("growpi.sensors.ds18b20.get_utc_datetime", return_value="2023-01-01T00:00:00Z")
def test_read_data_success(mock_datetime, mock_glob, mock_file):
    # Arrange
    mock_glob.return_value = ["/sys/bus/w1/devices/28-0000065b1a2c"]
    sensor = DS18B20(pin=4, name="TestSensor")

    # Act
    result = sensor.read_data()

    # Assert
    assert result["sensor"] == "TestSensor"
    assert result["temperature"] == 21.6
    assert result["reading_timestamp_utc"] == "2023-01-01T00:00:00Z"


@patch("growpi.sensors.ds18b20.glob.glob")
@patch("growpi.sensors.ds18b20.get_utc_datetime", return_value="2023-01-01T00:00:00Z")
def test_read_data_sensor_not_found(mock_datetime, mock_glob):
    # Arrange
    mock_glob.return_value = []
    sensor = DS18B20(pin=4, name="TestSensor")

    # Act
    result = sensor.read_data()

    # Assert
    assert result["sensor"] == "TestSensor"
    assert result["error"] == "Sensor not found"
    assert result["reading_timestamp_utc"] == "2023-01-01T00:00:00Z"


@patch("builtins.open", new_callable=mock_open, read_data="YES\n t=-5000")
@patch("growpi.sensors.ds18b20.glob.glob")
@patch("growpi.sensors.ds18b20.get_utc_datetime", return_value="2023-01-01T00:00:00Z")
def test_read_data_negative_temperature(mock_datetime, mock_glob, mock_file):
    # Arrange
    mock_glob.return_value = ["/sys/bus/w1/devices/28-0000065b1a2c"]
    sensor = DS18B20(pin=4, name="TestSensor")

    # Act
    result = sensor.read_data()

    # Assert
    assert result["sensor"] == "TestSensor"
    assert result["temperature"] == -5.0
    assert result["reading_timestamp_utc"] == "2023-01-01T00:00:00Z"


@patch("builtins.open", new_callable=mock_open, read_data="YES\n t=")
@patch("growpi.sensors.ds18b20.glob.glob")
def test_read_data_missing_temperature(mock_glob, mock_file):
    # Arrange
    mock_glob.return_value = ["/sys/bus/w1/devices/28-0000065b1a2c"]
    sensor = DS18B20(pin=4, name="TestSensor")

    # Act
    result = sensor.read_data()

    # Assert
    assert result is None


@patch("builtins.open", new_callable=mock_open, read_data="YES\n t=not_a_number")
@patch("growpi.sensors.ds18b20.glob.glob")
def test_read_data_invalid_temperature_format(mock_glob, mock_file):
    # Arrange
    mock_glob.return_value = ["/sys/bus/w1/devices/28-0000065b1a2c"]
    sensor = DS18B20(pin=4, name="TestSensor")

    # Act & Assert
    with pytest.raises(ValueError):
        sensor.read_data()
