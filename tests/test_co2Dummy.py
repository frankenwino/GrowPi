import pytest
from unittest.mock import patch
from sensors.co2Dummy import CO2Dummy

@pytest.fixture
def co2_sensor():
    return CO2Dummy(pin=21, name="CO2Dummy")

def test_init_sets_attributes(co2_sensor):
    assert co2_sensor.pin == 21
    assert co2_sensor.name == "CO2Dummy"

@patch("sensors.co2Dummy.get_utc_datetime", return_value="2024-01-01T00:00:00Z")
@patch("sensors.co2Dummy.random.randint", return_value=1234)
def test_read_data_returns_expected_dict(mock_randint, mock_get_utc_datetime, co2_sensor):
    data = co2_sensor.read_data()
    assert data["sensor"] == "CO2Dummy"
    assert data["ppm"] == 1234
    assert data["reading_timestamp_utc"] == "2024-01-01T00:00:00Z"

@patch("sensors.co2Dummy.random.randint")
def test_read_data_ppm_range(mock_randint, co2_sensor):
    # Test edge values
    for value in [999, 5050]:
        mock_randint.return_value = value
        data = co2_sensor.read_data()
        assert data["ppm"] == value

def test_read_data_sensor_name_and_keys(co2_sensor):
    with patch("sensors.co2Dummy.random.randint", return_value=2000), \
         patch("sensors.co2Dummy.get_utc_datetime", return_value="now"):
        data = co2_sensor.read_data()
        assert set(data.keys()) == {"sensor", "ppm", "reading_timestamp_utc"}
        assert data["sensor"] == "CO2Dummy"
        assert data["ppm"] == 2000
        assert data["reading_timestamp_utc"] == "now"