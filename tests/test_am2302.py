import pytest
from unittest.mock import MagicMock, patch
from growpi.sensors.am2302 import AM2302


@pytest.fixture
def mock_sensor():
    """Fixture to create a mock sensor."""
    mock = MagicMock()
    mock.temperature = 25.5
    mock.humidity = 60.2
    return mock


@pytest.fixture
def am2302_sensor(mock_sensor):
    """Fixture to create an AM2302 instance with a mock sensor."""
    with patch("growpi.sensors.am2302.adafruit_dht.DHT22", return_value=mock_sensor):
        return AM2302(pin=23, name="TestSensor")


def test_am2302_initialization(am2302_sensor):
    """Test the initialization of the AM2302 sensor."""
    # Assert
    assert am2302_sensor.pin == 23
    assert am2302_sensor.name == "TestSensor"


def test_am2302_read_data_success(am2302_sensor, mock_sensor):
    """Test successful reading of data from the sensor."""
    # Arrange/Act
    data = am2302_sensor.read_data()

    # Assert
    assert data is not None
    assert data["sensor"] == "TestSensor"
    assert data["temperature"] == round(mock_sensor.temperature, 2)
    assert data["humidity"] == round(mock_sensor.humidity, 2)
    assert "reading_timestamp_utc" in data


def test_am2302_read_data_failure():
    """Test failure to read data from the sensor."""
    # Arrange
    with patch("growpi.sensors.am2302.adafruit_dht.DHT22") as mock_dht:
        mock_dht.return_value.temperature = None
        mock_dht.return_value.humidity = None
        sensor = AM2302(pin=23, name="TestSensor")

        # Act
        data = sensor.read_data()

        # Assert
        assert data is None


def test_am2302_invalid_pin():
    """Test initialization with an invalid pin."""
    # Arrange/Act
    with pytest.raises(ValueError, match="Pin D99 not found on board module."):
        AM2302(pin=99, name="InvalidSensor")
