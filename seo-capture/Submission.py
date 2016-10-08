# This file implements a Submit object that sends imaging Session requests
# to the local queue Server
import zmq
import time
import Session
import json

class Submission(object):

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
        self.socket.send_string(self.serialize(session))
        return self

    def recv(self) -> str:
        self.socket.recv()

    def serialize(self, session: Session) -> list:
        ser = {}
        ser['targets'] = json.dumps(session.targets)
        ser['exposure_time'] = json.dumps(session.exposure_time)
        ser['exposure_count'] = json.dumps(session.exposure_count)
        ser['rgb'] = json.dumps(session.rgb)
        ser['binning'] = json.dumps(session.binning)
        ser['user'] = json.dumps(session.user)
        ser['close_after'] = json.dumps(session.close_after)
        ser['test_only'] = json.dumps(session.test_only)
        return json.dumps(ser)

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
    s = Submission().connect()
    session = Session.Session(['m31'], 60)
    s.submit(session)
    # print(s.serialize(session))
    # for request in range (1,10):
    #     s.submit("Hello")
    #     message = s.recv()
    #     print("Received reply "+str(request)+"["+str(message)+"]")
