import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from strategies.abstract_strategy import ExtractStrategy


class Extract:

    def __init__(self, strategy: ExtractStrategy):
        """
        Initialize the Extract class.

        Parameters:
        strategy (ExtractStrategy): The strategy used for data extraction.
        """
        self._strategy = strategy

    @property
    def strategy(self) -> ExtractStrategy:
        """
        Get the current extraction strategy.

        Returns:
        ExtractStrategy: The current strategy instance used for data extraction.
        """
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: ExtractStrategy) -> None:
        """
        Set a new extraction strategy.

        Parameters:
        strategy (ExtractStrategy): The new strategy instance for data extraction.
        """
        self._strategy = strategy

    def retrieve_data(self):
        """
        Retrieve specific data using the current extraction strategy.

        Returns:
        The data retrieved by the strategy. The exact type of the data depends
        on the implementation of the extraction strategy.
        """
        return self._strategy.retrive_data()
