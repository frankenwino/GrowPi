# """Main module."""
# # print("Hello, GrowPi!")
import json
from sensors.sensor_factory import create_sensor
# from utils.api_handler import post_data

def load_sensors_from_config(config_file="sensors.json"):
    """Loads sensor configurations from a JSON file and initializes them."""
    with open(config_file, "r") as file:
        sensor_configs = json.load(file)
    
    sensors = []
    for config in sensor_configs:
        sensor_type = config.pop("type")
        sensor = create_sensor(sensor_type, **config)
        sensors.append(sensor)
    
    return sensors

def main():
    sensors = load_sensors_from_config()

    for sensor in sensors:
        try:
            data = sensor.read_data()
            print(data)
            # response = post_data(data)
            # print(f"Data from {sensor.__class__.__name__} posted successfully:", response)
        except Exception as e:
            print(f"Error with {sensor.__class__.__name__}:", e)

if __name__ == "__main__":
    main()
