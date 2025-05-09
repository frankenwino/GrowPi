import pytest
from unittest.mock import MagicMock, patch
from growpi.sensors.am2301 import AM2301


@pytest.fixture
def mock_sensor():
    """Fixture to create a mock sensor."""
    mock = MagicMock()
    mock.temperature = 25.5
    mock.humidity = 60.2
    return mock


@pytest.fixture
def am2301_sensor(mock_sensor):
    """Fixture to create an AM2301 instance with a mock sensor."""
    with patch("growpi.sensors.am2301.adafruit_dht.DHT21", return_value=mock_sensor):
        return AM2301(pin=20, name="TestSensor")


def test_am2301_initialization(am2301_sensor):
    """Test the initialization of the AM2301 sensor."""
    # Assert
    assert am2301_sensor.pin == 20
    assert am2301_sensor.name == "TestSensor"


def test_am2301_read_data_success(am2301_sensor, mock_sensor):
    """Test successful reading of data from the AM2301 sensor."""
    # Arrange
    with patch(
        "growpi.sensors.am2301.get_utc_datetime", return_value="2023-01-01T00:00:00Z"
    ):
        # Act
        data = am2301_sensor.read_data()

    # Assert
    assert data is not None
    assert data["sensor"] == "TestSensor"
    assert data["temperature"] == 25.5
    assert data["humidity"] == 60.2
    assert data["date_time_utc"] == "2023-01-01T00:00:00Z"


def test_am2301_read_data_failure(am2301_sensor, mock_sensor):
    """Test failure in reading data from the AM2301 sensor."""
    # Arrange
    mock_sensor.temperature = None
    mock_sensor.humidity = None

    # Act
    data = am2301_sensor.read_data()

    # Assert
    assert data is None


def test_am2301_invalid_pin():
    """Test initialization with an invalid GPIO pin."""
    # Arrange/Act
    with pytest.raises(ValueError, match="Pin D99 not found in board module."):
        AM2301(pin=99, name="InvalidSensor")
