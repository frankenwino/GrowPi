from fastapi import FastAPI
from sensor_check import load_sensors_from_config

app = FastAPI()

sensors = load_sensors_from_config()


@app.get("/")
async def read_root():
    return {"msg": "GrowPi API is running"}


@app.get("/sensors")
async def list_sensors():
    """List all available sensors and their types."""
    return {"available_sensors": [sensor.__class__.__name__ for sensor in sensors]}


@app.get("/sensor/{sensor_name}")
async def get_sensor_reading(sensor_name: str):
    """Fetch data from a specific sensor by name."""
    for sensor in sensors:
        if sensor.__class__.__name__.lower() == sensor_name.lower():
            return sensor.read_data()

    return {"error": f"Sensor '{sensor_name}' not found"}
