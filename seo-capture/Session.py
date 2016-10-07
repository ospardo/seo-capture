from typing import List, Union
from Util import find_value
import os

class Session(object):
    """
    This class represents a single imaging session that will image each target with 
    the chosen number of exposures where each exposure is exposure_time seconds long.
    By default, science frames with each of the three primary filters will be taken, 
    as well as clear darks, biases and flats. 
    """
    
    def __init__(self, targets: List[str],
                 exposure_time: float,
                 exposure_count: int = 1,
                 rgb: bool = True,
                 binning: int = 2,
                 user: str = "",
                 close_after: bool = True, 
                 test_only: bool = False):
        """ Creates a new imaging session with desired parameters.

        Creates a new imaging session that will image each target with exposure_count 
        exposures where each exposure is exposure_time seconds long. 

        Args:
            targets: a list of strings identifying targets to be imaged, i.e.
                    ['m31, 'C 34', 'NGC 6974']
            exposure_time: the time for each exposure in seconds
            exposure_count: the number of exposures to take for each filter
            rgb: whether to take images with each of the primary filters
            user: the username of the user who requested/created the session
            close_after: whether the dome should close at the end of the session
            test_only: if this is True, telescope control commands will be
                    printed to STDOUT and NOT executed. Useful for debugging.

        """
        
        # A list of strings containing catalog names of objects to be imaged
        # Currently, the objects are imaged in the order they are specified.
        self.targets = []

        # The exposure time in seconds for each science image
        self.exposure_time = exposure_time

        # The number of science images to be taken per filter/clear
        self.exposure_count = exposure_count

        # Whether R, G, B filters should be used 
        self.rgb = rgb

        # What binning to use
        self.binning = binning

        # The user who created the session
        if user == "": # take environment variable if not specified
            self.user = os.environ['USER']
        else:
            self.user = user

        # Whether this is a trial, test_only run
        self.test_only = test_only

    def execute(self) -> int: 
        """ Starts the execution of the imaging session; return's status
        once imaging run is completed. 
        """
        pass

    def add_target(self, target: Union[str, List[str]]) -> 'Session':
        """ Adds an additional list of targets to a session. Currently cannot 
        be called after the session has started executing. 

        N.B. Return type signature is a to-be-processed forward reference
        to the Session class (as the Session class has yet to be added to
        the namespace and therefore can't be used as a type hint)
        """
        self.targets.append(target)
        return self

    def set_exposure_time(self, exposure_time: float) -> 'Session':
        """ Changes the exposure time of the imaging session to a new value
        """
        self.exposure_time = exposure_time
        return self

    def set_exposure_count(self, exposure_count: int) -> 'Session':
        """ Changes the exposure count of the imaging session to a new value
        """
        self.exposure_count = exposure_count
        return self

    def __run_command(self, command: str) -> int:
        """ Executes a shell command either locally, or remotely via ssh. 
        Returns the status code of the shell command upon completion. 
        """
        if self.test_only == True:
            print(command)
    
    def __weather_ok(self) -> bool:
        """ Checks whether the sun has set, there is no rain (rain=0) and that 
        it is less than 40% cloudy. Returns true if the weather is OK to open up, 
        false otherwise. 
        """

        # check sun
        sun = self.__run_command("sun")
        if float(find_value("alt", sun)) >= -1.0:
            return False

        # sun is good - check for weather
        weather = self.__run_command("tx taux")

        # if this cmd failed, return false to be safe
        if weather == None or weather == "":
            return False
        
        rain = 1 # default to being raining just in case
        cloud = 1 # default to being cloudy just in case
        rain = float(find_value("rain", weather)) # find rain=val
        cloud = float(find_value("cloud", weather)) # find cloud=val

        if rain == 0 and cloud < 0.4:
            return True
        else:
            return False
    
    def __open_dome(self) -> bool:
        """ Checks that the weather is acceptable, and then opens the dome, 
        if it is not already open, and  also enables tracking. 
        """
        # check if dome is already open
        if self.__dome_status() == True:
            return True

        # check that weather is OK to open
        if self.__weather_ok() == True:
            result = self.__run_command("openup nocloud &&" 
                                        "keepopen maxtime=20000 slit"
                                        "&& track on")
            if result == True: # everything was good
                return True
            else: # one of the commands failed
                return False
        else:
            return False

    def __dome__status(self) -> bool:
        """ Checks whether the slit is open or closed. Returns True if open, 
        False if closed.
        """
        slit = self.__run_command("tx slit")
        result = find_value("slit", slit)
        if result == "open":
            return True

        return False

    def __goto_target(self, target: str) -> bool:
        """ Points the telescope at the target in question. Returns True if
        successfully (object was visible), and returns False if unable to set
        telescope (failure, object not visible).
        """
        if self.__target_visible(target) == True:
            cmd = "catalog "+target+" | dopoint"
            return self.__run__command(cmd)

        return False

    def __target_visible(self, target: str) -> bool:
        """ Checks whether a target is visible, and whether it is > 40 degrees
        in altitude. Returns True if visible and >40, False otherwise
        """
        cmd = "catalog "+target+" | altaz"
        altaz = self.__run_command(cmd).split()
        if float(find_value("alt", altaz)) >= 40:
            return True

        return False

    def __current_filter(self) -> str:
        """ Returns the name of the currently enabled filter, or
        clear otherwise. 
        """
        return self.__run_command("pfilter")
        
    def __change_filter(self, name: str) -> bool:
        """ Changes filter to the new specified filter. Options are: 
        u, g, r, i, z, clear, h-alpha. Returns True if successful, 
        False otherwise
        """
        if name == "h-alpha":
            return self.__run_command("pfilter h-alpha")
        else:
            return self.__run_command("pfilter "+name+"-band")

    def __take_exposure(self, filename: str) -> bool:
        """ Takes an exposure of length self.exposure_time saves it in the FITS 
        file with the specified filename. Returns True if imaging
        was successful, False otherwise. 
        """
        cmd = "image time="+self.exposure_time+" bin="+self.binning+" "
        cmd += "outfile="+filename+".fits"
        status = self.__run_command(cmd)
        return status

    def __take_bias(self, filename: str) -> bool:
        """ Takes a bias frame and saves it in the FITS file with the specified
        filename. Returns True if imaging was successful, False otherwise. 
        """
        cmd = "image time=0.5 bin="+self.binning+" "
        cmd += "outfile="+filename+"_BIAS.fits"
        status = self.__run_command(cmd)
        return status

    def __take_dark(self, filename: str) -> bool:
        """ Takes an dark exposure of length self.exposure_time saves it in the
        FITS file with the specified filename. Returns True if imaging
        was successful, False otherwise. 
        """
        cmd = "image time="+self.exposure_time+" bin="+self.binning+" dark "
        cmd += "outfile="+filename+"_DARK.fits"
        status = self.__run_command(cmd)
        return status

if __name__ == '__main__':
    s = Session(['m31'], 60, 5, test_only=True)
