from fastapi.testclient import TestClient
import main
from main import app

client = TestClient(app)


def test_read_main():
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"msg": "GrowPi API is running"}


def test_list_sensors_with_valid_api_key(monkeypatch):
    # Arrange
    monkeypatch.setenv("API_KEYS", "test_key")

    # Act
    response = client.get("/sensors", headers={"x-api-key": "test_key"})

    # Assert
    assert response.status_code == 200
    assert "available_sensors" in response.json()
    assert isinstance(response.json()["available_sensors"], list)


def test_list_sensors_with_invalid_api_key():
    # Act
    response = client.get("/sensors", headers={"x-api-key": "invalid_key"})

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}


def test_list_sensors_without_api_key():
    # Act
    response = client.get("/sensors")

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}


def test_get_sensor_reading_with_valid_api_key(monkeypatch):
    # Arrange
    monkeypatch.setenv("API_KEYS", "test_key")

    class MockSensor:
        def read_data(self):
            return {"temperature": 25, "humidity": 60}

    MockSensor.__name__ = "MockSensor"
    monkeypatch.setattr(main, "sensors", [MockSensor()])

    # Act
    response = client.get("/sensor/MockSensor", headers={"x-api-key": "test_key"})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"temperature": 25, "humidity": 60}


def test_get_sensor_reading_with_invalid_api_key(monkeypatch):
    # Arrange
    monkeypatch.setenv("API_KEYS", "test_key")

    class MockSensor:
        def read_data(self):
            return {"temperature": 25, "humidity": 60}

    MockSensor.__name__ = "MockSensor"
    monkeypatch.setattr(main, "sensors", [MockSensor()])

    # Act
    response = client.get("/sensor/MockSensor", headers={"x-api-key": "invalid_key"})

    # Assert
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid or missing API Key"}


def test_get_sensor_reading_with_non_existent_sensor(monkeypatch):
    # Arrange
    monkeypatch.setenv("API_KEYS", "test_key")
    monkeypatch.setattr("main.sensors", [])

    # Act
    response = client.get(
        "/sensor/NonExistentSensor", headers={"x-api-key": "test_key"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"error": "Sensor 'NonExistentSensor' not found"}
