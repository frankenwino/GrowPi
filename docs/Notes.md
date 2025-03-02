# Creating a new sensor

Create a sensor class in /src/growpi/sensors/
It needs to sublass Sensor eg:

```python
from sensors.sensor_interface import Sensor

class LM393(Sensor):
```

Add the new sensor class to `/src/growpi/sensor_factory.py`

Add the sensor configuration to `src/growpi/sensors.json`