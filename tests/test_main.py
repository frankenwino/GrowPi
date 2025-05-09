from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "GrowPi API is running"}


def test_list_sensors_with_valid_api_key(monkeypatch):
    # Mock the API_KEYS environment variable
    monkeypatch.setenv("API_KEYS", "test_key")

    # Pass the valid API key in the query parameter
    response = client.get("/sensors", headers={"x-api-key": "test_key"})
    assert response.status_code == 200
    assert "available_sensors" in response.json()
    assert isinstance(response.json()["available_sensors"], list)


def test_list_sensors_with_invalid_api_key():
    # Pass an invalid API key
    response = client.get("/sensors", headers={"x-api-key": "invalid_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}


def test_list_sensors_without_api_key():
    # Do not pass any API key
    response = client.get("/sensors")
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}

    def test_get_sensor_reading_with_valid_api_key(monkeypatch):
        # Mock the API_KEYS environment variable
        monkeypatch.setenv("API_KEYS", "test_key")

        # Mock the sensors list with a fake sensor
        class MockSensor:
            def __class__(self):
                return self

            def __name__(self):
                return "MockSensor"

            def read_data(self):
                return {"temperature": 25, "humidity": 60}

        monkeypatch.setattr("main.sensors", [MockSensor()])

        # Pass the valid API key and request the sensor data
        response = client.get("/sensor/MockSensor", headers={"x-api-key": "test_key"})
        assert response.status_code == 200
        assert response.json() == {"temperature": 25, "humidity": 60}


def test_get_sensor_reading_with_invalid_api_key(monkeypatch):
    # Mock the API_KEYS environment variable
    monkeypatch.setenv("API_KEYS", "test_key")

    # Mock the sensors list with a fake sensor
    class MockSensor:
        def __class__(self):
            return self

        def __name__(self):
            return "MockSensor"

        def read_data(self):
            return {"temperature": 25, "humidity": 60}

    monkeypatch.setattr("main.sensors", [MockSensor()])

    # Pass an invalid API key and request the sensor data
    response = client.get("/sensor/MockSensor", headers={"x-api-key": "invalid_key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}


def test_get_sensor_reading_with_non_existent_sensor(monkeypatch):
    # Mock the API_KEYS environment variable
    monkeypatch.setenv("API_KEYS", "test_key")

    # Mock the sensors list with no matching sensor
    monkeypatch.setattr("main.sensors", [])

    # Pass the valid API key and request a non-existent sensor
    response = client.get(
        "/sensor/NonExistentSensor", headers={"x-api-key": "test_key"}
    )
    assert response.status_code == 200
    assert response.json() == {"error": "Sensor 'NonExistentSensor' not found"}
