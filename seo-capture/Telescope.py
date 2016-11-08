# This file provides an abstraction around the control commands for the telescope; no shell commands
# should be run except through the Telescope interface provided below

import typing
import subprocess
import Util

class Telescope(object):

    def __init__(self):
        pass

    
    def open_dome(self) -> bool:
        pass

    
    def close_dome(self) -> bool:
        pass

    
    def weather_ok(self) -> bool:
        pass

    
    def dome_status(self) -> str:
        pass

    
    def goto_target(self, name: str) -> bool:
        pass

    
    def target_visible(self, name: str) -> bool: 
        pass

    
    def current_filter(self) -> str:
        pass

    
    def change_filter(self, name: str) -> str:
        pass

    
    def take_exposure(self, filename: str) -> bool:
        pass

    
    def take_bias(self, filename: str) -> bool:
        pass

    
    def take_dark(self, filename: str) -> bool:
        pass

    
    def enable_tracking(self) -> bool:
        pass

    
    def focus(self) -> bool:
        pass

    
    def enable_flats(self) -> bool:
        # run tin?
        pass

    
    def offset(self) -> bool:
        pass
    

    def __log(self, msg: str, color: str = "white") -> bool:
        """ Prints a log message to STDOUT. Returns True if successful, False
        otherwise.
        """
        return Util.log(msg, color)    

    
    def __run_command(self, command: str) -> str:
        """ Executes a shell command either locally, or remotely via ssh. 
        Returns the byte string representing the captured STDOUT
        """
        self.__log("Executing {}".format(command), color="magenta")
        try:
            return subprocess.check_output(command)
        except:
            self.__log("Failed while executing {}".format(command), color="red")
            self.__log("Please manually close the dome by running"
                       " `closedown` and `logout`.", color="red")
            exit(1)
