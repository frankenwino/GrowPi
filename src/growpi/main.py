from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
from sensor_check import load_sensors_from_config
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()
sensors = load_sensors_from_config()

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_keys() -> list[str]:
    keys = os.getenv("API_KEYS", "")
    return [k.strip() for k in keys.split(",") if k.strip()]

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    valid_keys = get_api_keys()
    
    if api_key_query in valid_keys:
        return api_key_query
    if api_key_header in valid_keys:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


@app.get("/")
async def read_root():
    return {"msg": "GrowPi API is running"}


@app.get("/private")
async def private(api_key: str = Security(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    return f"Private Endpoint. API Key: {api_key}"


@app.get("/sensors")
async def list_sensors(api_key: str = Security(get_api_key)):
    """List all available sensors and their types."""
    return {"available_sensors": [sensor.__class__.__name__ for sensor in sensors]}


@app.get("/sensor/{sensor_name}")
async def get_sensor_reading(sensor_name: str, api_key: str = Security(get_api_key)):
    """Fetch data from a specific sensor by name."""
    for sensor in sensors:
        if sensor.__class__.__name__.lower() == sensor_name.lower():
            return sensor.read_data()

    return {"error": f"Sensor '{sensor_name}' not found"}
