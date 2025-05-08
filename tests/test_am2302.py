import pytest
from unittest.mock import MagicMock, patch
from growpi.sensors.am2302 import AM2302


@pytest.fixture
def mock_sensor():
    """Fixture to mock the adafruit_dht.DHT22 sensor."""
    with patch("growpi.sensors.am2302.adafruit_dht.DHT22") as mock_dht:
        yield mock_dht


@pytest.fixture
def mock_utils():
    """Fixture to mock the get_utc_datetime utility."""
    with patch("growpi.sensors.am2302.get_utc_datetime", return_value="2023-01-01T00:00:00Z") as mock_datetime:
        yield mock_datetime


def test_am2302_read_data_success(mock_sensor, mock_utils):
    """Test successful reading of temperature and humidity."""
    # Mock sensor instance
    mock_instance = MagicMock()
    mock_instance.temperature = 22.3
    mock_instance.humidity = 55.7
    mock_sensor.return_value = mock_instance

    # Create AM2302 instance
    sensor = AM2302(pin=23, name="TestSensor")

    # Call read_data
    result = sensor.read_data()

    # Assertions
    assert result is not None, "Result should not be None"
    assert result["sensor"] == "TestSensor"
    assert result["temperature"] == 22.3
    assert result["humidity"] == 55.7
    assert result["date_time_utc"] == "2023-01-01T00:00:00Z"


def test_am2302_read_data_failure(mock_sensor):
    """Test failure when sensor returns None values."""
    # Mock sensor instance
    mock_instance = MagicMock()
    mock_instance.temperature = None
    mock_instance.humidity = None
    mock_sensor.return_value = mock_instance

    # Create AM2302 instance
    sensor = AM2302(pin=23, name="TestSensor")

    # Call read_data
    result = sensor.read_data()

    # Assertions
    assert result is None, "Result should be None on failure"


def test_am2302_invalid_pin():
    """Test initialization with an invalid pin."""
    with pytest.raises(ValueError, match="Pin D99 not found on board module."):
        AM2302(pin=99, name="InvalidPinSensor")

def test_am2302_partial_data(mock_sensor, mock_utils):
    """Test handling of partial data (temperature or humidity is None)."""
    # Mock sensor instance with partial data
    mock_instance = MagicMock()
    mock_instance.temperature = 24.5
    mock_instance.humidity = None
    mock_sensor.return_value = mock_instance

    # Create AM2302 instance
    sensor = AM2302(pin=23, name="TestSensor")

    # Call read_data
    result = sensor.read_data()

    # Assertions
    assert result is None, "Result should be None when partial data is received"
