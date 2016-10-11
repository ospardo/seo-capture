import typing
import time

def find_value(arg: str, string: str) -> str:
    """ Searches for "arg=X" in the string and returns X
    as a string
    """
    for s in string.split():
        if s[0:len(arg)+1] == arg+"=":
            return s[len(arg)+1:]

    return ""


def log( msg: str, color: str = "white") -> bool:
        """ Prints a log message to STDOUT. Returns True if successful, False
        otherwise.
        """
        colors = {"red":"31", "green":"32", "blue":"34", "cyan":"36",
                  "white":"37", "yellow":"33", "magenta":"34"}
        logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        log = "\033[1;"+colors[color]+"m"+logtime+" SESSION: "+msg+"\033[0m"
        print(log)
        return True

