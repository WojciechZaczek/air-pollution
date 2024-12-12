from abc import ABC, abstractmethod

class ExtractStrategy(ABC):

    @abstractmethod
    def retrive_data(self):
        pass