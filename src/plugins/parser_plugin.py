from abc import ABC, abstractmethod

class Parser_Plugin(ABC):
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def process(self, data_to_process)-> dict:
        """Process input string to dict

        This method is used to parse the input from different data sources.
        Output should be what has to be written to the database with keys as
        referring to column names and values for values.

        Args:
            data_to_process: data that should be processed in the format
                that is written to Event Hub.

        """
        pass

    # @abstractmethod
    # def get_keys(self)-> list:
    #     pass
