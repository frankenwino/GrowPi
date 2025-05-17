import pytest
from unittest.mock import patch
from sensors.phDummy import PHDummy

@pytest.fixture
def ph_sensor():
    return PHDummy(pin=21, name="TestPHSensor")

@patch("sensors.phDummy.get_utc_datetime")
@patch("sensors.phDummy.random.uniform")
def test_read_data_returns_expected_keys(mock_random, mock_get_utc_datetime, ph_sensor):
    mock_random.return_value = 7.2
    mock_get_utc_datetime.return_value = "2024-01-01T00:00:00Z"
    data = ph_sensor.read_data()
    assert set(data.keys()) == {"sensor", "ph", "reading_timestamp_utc"}
    assert data["sensor"] == "TestPHSensor"
    assert data["ph"] == 7.2
    assert data["reading_timestamp_utc"] == "2024-01-01T00:00:00Z"

@patch("sensors.phDummy.random.uniform")
def test_read_data_ph_range(mock_random, ph_sensor):
    # Test edge values
    for value in [5.0, 8.5]:
        mock_random.return_value = value
        data = ph_sensor.read_data()
        assert 5.0 <= data["ph"] <= 8.5

def test_phdummy_init_sets_attributes():
    sensor = PHDummy(pin=10, name="Dummy")
    assert sensor.pin == 10
    assert sensor.name == "Dummy"