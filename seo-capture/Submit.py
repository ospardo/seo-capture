# This file implements a Submit object that sends imaging Session requests
# to the local queue Server
import zmq
import time
import Session

class Submitter(object):

    def __init__(self, port: int = 27748):
        """ """
        self.__log("Creating a new Submitter...", color="green")
        # port to be used 
        self.port = port

        # create zmq context
        self.context = zmq.Context()

        # create socket
        self.socket = self.context.socket(zmq.REQ)

        
    def connect(self) -> 'Submitter':
        # connect to server
        self.socket.connect("tcp://localhost:%s" % self.port)
        self.__log("Connected to server on port %s" % self.port)
        return self
    
    def submit(self, session: Session) -> 'Submitter':
        self.socket.send_string(session)

    def recv(self) -> str:
        self.socket.recv()

    def __log(self, msg: str, color: str = "white") -> bool:
        """ Prints a log message to STDOUT. Returns True if successful, False
        otherwise.
        """
        colors = {"red":"31", "green":"32", "blue":"34", "cyan":"36",
                  "white":"37", "yellow":"33", "magenta":"34"}
        logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        log = "\033[1;"+colors[color]+"m"+logtime+" SUBMIT: "+msg+"\033[0m"
        print(log)
        return True


if __name__ == "__main__":
    s = Submitter().connect()
    for request in range (1,10):
        s.submit("Hello")
        message = s.recv()
        print("Received reply "+str(request)+"["+str(message)+"]")
