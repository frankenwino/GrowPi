from abc import ABC, abstractmethod


class Sensor(ABC):
    """
    Abstract base class for all sensors.

    This class defines the interface that all sensor classes must implement.
    Subclasses must provide an implementation for the `read_data` method.

    Methods
    -------
    read_data()
        Abstract method to read data from the sensor. Must be implemented by subclasses.
    """

    @abstractmethod
    def read_data(self):
        pass
