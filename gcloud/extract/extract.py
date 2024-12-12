import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from strategies.abstract_strategy import ExtractStrategy


class Extract:

    def __init__(self, strategy: ExtractStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> ExtractStrategy:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ExtractStrategy):
        self._strategy = strategy

    def retrieve_data(self):
        return self._strategy.retrive_data()