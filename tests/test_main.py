from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "GrowPi API is running"}


def test_list_sensors():
    response = client.get("/sensors")
    assert response.status_code == 200
    assert "available_sensors" in response.json()
    assert len(response.json()["available_sensors"]) > 0


def test_get_sensor_reading():
    response = client.get("/sensor/lm393")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_non_existent_sensor():
    response = client.get("/sensor/non_existent_sensor")
    assert response.status_code == 200
    assert response.json() == {"error": "Sensor 'non_existent_sensor' not found"}
