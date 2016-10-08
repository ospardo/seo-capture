import json
import time
import typing

class Executor(object):
    """ This class is responsible for executing and scheduling a 
    list of Sessions stored in the JSON queue constructed by the Server. 
    """

    def __init__(self, filename: str):
        """ This creates a new executor to execute a single nights
        list of Sessions stored in the JSON file specified by filename. 
        """

        # filename to be read
        self.filename = filename

        # load queue from disk
        self.sessions = self.load_queue(self.filename)

        
    def load_queue(self, filename: str) -> list:
        """ This loads a JSON queue file into a list of Python session
        objects that can then be executed. 
        """
        pass

