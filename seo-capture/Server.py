# This file implements a Server that listens for requests from Submit programs
# to add Sessions to the queue for tonight's imaging session
import zmq
import time
import typing

class Server(object):
    """ This class represents a server that listens for queueing requests from 
    clients; once it has received a request, process_message() is called, which
    adds the request to the queue.
    """

    def __init__(self, port: int = 27748):
        """ This creates a new server listening on the specified port; this does
        not start the server listening, it just creates the server. start() must
        be called for the server to be initialized. 

        port: the port to listen on
        """
        self.__log("Creating new queue server...", color="green")
        # the port to be used for communication
        self.port = str(port)

        # zeroMQ context
        self.context = zmq.Context()

        # zeroMQ socket
        self.socket = self.context.socket(zmq.REP)

        # connect socket
        self.socket.bind("tcp://*:%s" % self.port)
        self.__log("Bound server to socket %s" % self.port)

        # file name for JSON store
        currdate = time.strftime("%Y-%m-%d", time.gmtime())
        self.filename = currdate+"_queue.json"
        self.__log("Storing queue in %s" % self.filename)

        
    def start(self):
        """ Starts the servers listening for new requests; server blocks
        on the specified port until it receives a request
        """
        while True:
            message = self.socket.recv()
            self.process_message(message)
            self.__log("Received message from a client...")
            time.sleep(1)
            self.socket.send_string("RECEIVED")

    def __log(self, msg: str, color: str = "white") -> bool:
        """ Prints a log message to STDOUT. Returns True if successful, False
        otherwise.
        """
        colors = {"red":"31", "green":"32", "blue":"34", "cyan":"36",
                  "white":"37", "yellow":"33", "magenta":"34"}
        logtime = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        log = "\033[1;"+colors[color]+"m"+logtime+" SERVER: "+msg+"\033[0m"
        print(log)
        return True


    def process_message(self, msg: str) -> list:
        pass
    

if __name__ == "__main__":
    server = Server()
    server.start()
