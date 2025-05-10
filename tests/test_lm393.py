import pytest
from unittest.mock import patch, MagicMock
from growpi.sensors.lm393 import LM393


@pytest.fixture
def mock_gpio():
    with patch("growpi.sensors.lm393.GPIO") as mock_gpio:
        yield mock_gpio


@pytest.fixture
def mock_get_utc_datetime():
    with patch(
        "growpi.sensors.lm393.get_utc_datetime", return_value="2023-01-01T00:00:00Z"
    ) as mock_datetime:
        yield mock_datetime


@pytest.fixture
def lm393_sensor(mock_gpio):
    return LM393(pin=21, name="LM393")


def test_lm393_initialization(mock_gpio):
    # Arrange
    pin = 21
    name = "LM393"

    # Act
    sensor = LM393(pin=pin, name=name)

    # Assert
    mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
    mock_gpio.setup.assert_called_once_with(pin, mock_gpio.IN)


def test_read_data_light_detected(mock_gpio, mock_get_utc_datetime, lm393_sensor):
    # Arrange
    mock_gpio.input.return_value = 0  # Simulate light detected

    # Act
    data = lm393_sensor.read_data()

    # Assert
    assert data["sensor"] == "LM393"
    assert data["light_detected"] is True
    assert data["reading_timestamp_utc"] == "2023-01-01T00:00:00Z"


def test_read_data_no_light_detected(mock_gpio, mock_get_utc_datetime, lm393_sensor):
    # Arrange
    mock_gpio.input.return_value = 1  # Simulate no light detected

    # Act
    data = lm393_sensor.read_data()

    # Assert
    assert data["sensor"] == "LM393"
    assert data["light_detected"] is False
    assert data["reading_timestamp_utc"] == "2023-01-01T00:00:00Z"
