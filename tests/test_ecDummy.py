import pytest
from unittest.mock import patch
from sensors.ecDummy import ECDummy

@pytest.fixture
def ec_dummy():
    return ECDummy(pin=21, name="ECDummy")

def test_init_sets_attributes(ec_dummy):
    assert ec_dummy.pin == 21
    assert ec_dummy.name == "ECDummy"

@patch("sensors.ecDummy.get_utc_datetime")
@patch("sensors.ecDummy.random.uniform") 
def test_read_data_returns_expected_dict(mock_uniform, mock_get_utc_datetime, ec_dummy):
    mock_uniform.return_value = 1.234
    mock_get_utc_datetime.return_value = "2024-06-01T12:00:00Z"
    data = ec_dummy.read_data()
    assert data["sensor"] == "ECDummy"
    assert data["mScm"] == round(1.234, 1)
    assert data["reading_timestamp_utc"] == "2024-06-01T12:00:00Z"

@patch("sensors.ecDummy.random.uniform")
def test_read_data_mScm_range(mock_uniform, ec_dummy):
    # Test edge values
    for value in [0.0, 2.9]:  # Changed to 0.0 to ensure float type
        mock_uniform.return_value = value
        data = ec_dummy.read_data()
        assert 0 <= data["mScm"] <= 2.9
        assert isinstance(data["mScm"], float)

@patch("sensors.ecDummy.random.uniform")
def test_read_data_mScm_precision(mock_uniform, ec_dummy):
    # Test rounding to 1 decimal place
    test_values = [1.234, 2.897, 0.001]
    for value in test_values:
        mock_uniform.return_value = value
        data = ec_dummy.read_data()
        assert str(data["mScm"]).count('.') == 1
        assert len(str(data["mScm"]).split('.')[1]) == 1

@patch("sensors.ecDummy.get_utc_datetime")
def test_read_data_timestamp_format(mock_get_utc_datetime, ec_dummy):
    # Test timestamp format
    mock_get_utc_datetime.return_value = "2024-06-01T12:00:00Z"
    data = ec_dummy.read_data()
    assert "reading_timestamp_utc" in data
    assert isinstance(data["reading_timestamp_utc"], str)
    assert "T" in data["reading_timestamp_utc"]
    assert "Z" in data["reading_timestamp_utc"]

def test_sensor_name_validation(ec_dummy):
    # Test sensor name is not empty
    assert ec_dummy.name != ""
    assert isinstance(ec_dummy.name, str)

def test_pin_validation(ec_dummy):
    # Test pin number is valid
    assert isinstance(ec_dummy.pin, int)
    assert ec_dummy.pin > 0