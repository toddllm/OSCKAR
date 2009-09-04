import SocketServer
import threading
import sys
sys.path.append('/usr/local/share/osckar/lib/')
import comm as c

#Global variables
eventHandlerSockets = {}
eHSlock = threading.Lock()
comm = c.Comm()
PROCEDURE_LENGTH = 6        

# EventChat Request Handler Class
# Processes signals over a socket
# Manages map of Event Handler Sockets (persistent connection to event handlers)
#      mapping is between handlers and eventNames
class ECRequestHandler(SocketServer.BaseRequestHandler):

    # setup is called before the handle() method to perform any initialization 
    # actions required.
    def setup(self):
        print self.client_address, 'connected!'
        self.request.send('helloo')


    # The handle function does all the work required to service a request.
    # Several instance attributes are available to it; the request is 
    # available as self.request; the client address as self.client_address; 
    # and the server instance as self.server, in case it needs access to 
    # per-server information.
    def handle(self):
        while 1:
            #do a try catch for various network related exception,
            #the exceptions are handled gracefully--just keep running
            try:
                #listen for a procdure call, of fixed length
                procedure = self.request.recv(PROCEDURE_LENGTH)
                print "DEBUG:::procedure:::", procedure + ":::"
                
                # if a connect breaks during processing, the recv will
                # return nothing and procedure will be false
                # this is also common for nonpersistent clients
                # (clients that just signal and quit)
                #check for those cases here
                if not procedure:
                    print self.client_address, 'connection broken!'
                    break 
                
                # someone is trying to register as a handler for an event
                if procedure == 'regevt':  
                    self.doRegisterEvent()
                    
                # someone is trying to signal an event
                elif procedure == 'signal': # 
                    self.doSignalEvent()

                # someone is gracefully removing themselves as a handler
                elif procedure == 'byebye':
                    self.doRemoveHandler()
            
            #TODO: add a DEBUG mode to allow raising various events
            #add except cases for debugging, remove for production
            ###
            except(NameError):
                raise

            except(TypeError):
                raise
            ###
            #leave these are in place to be a catch all, even in production
            except(ValueError):
                print 'Malformed data recieved', sys.exc_info()[0]
            except:
                print 'There was a general (probably network) error.',
                print 'For your convenience, we ignored this:',sys.exc_info()[0]
        return


    # finish is called after the handle() method to perform any clean-up actions 
    # If setup() or handle() raise an exception, this function will not be called.
    def finish(self):
        print self.client_address, 'disconnected!'
        self.doRemoveHandler()

    # Called during a regevt procedure call
    def doRegisterEvent(self):
        #read the EventName over the socket
        eventName = comm.readChunk(self.request)
        try:
            # lock event handler map
            eHSlock.acquire() 
            # check if this is a new eventName
            if eventName not in eventHandlerSockets:
                # add an empty list for this mapping 
                eventHandlerSockets[eventName] = []
            # Add this socket as a listener for this eventName
            eventHandlerSockets[eventName].append(self.request)
        finally:
            # unlock event handler map
            # handled in the finally to be more graceful
            eHSlock.release()  
        print self.client_address, 'now listening to event', eventName

    # Called during a signal procedure call
    def doSignalEvent(self):
        # read eventName from the socket
        eventName = comm.readChunk(self.request)
        print "DEBUG: eventName ",  eventName
        # read event arguments from the socket
        eventArgs = comm.readChunk(self.request)
        print "DEBUG: eventArgs: ", eventArgs

        # check if we have a handler for this event
        if eventName in eventHandlerSockets and \
                len(eventHandlerSockets[eventName]) > 0:
            #for each handler of this event
            for handler in eventHandlerSockets[eventName]: 
                try:
                    # singal the handler
                    handler.send('signal' + comm.makeChunk(eventName) +\
                                     comm.makeChunk(eventArgs))
                except:
                    print 'Error signaling one of the listeners.'
                    print 'We will ignore it this time:',sys.exc_info()[0]
            # end for each handler of this event
            print self.client_address, 'has signaled event', eventName
        else:
            print self.client_address, 'has signaled event', eventName,
            print 'but there are no listeners!'
            self.request.send('bounce' + comm.makeChunk(eventName))

    # Called during a byebye procedure call
    # Also used by finish() to do non-graceful cleanup
    def doRemoveHandler(self):
        try:
            eHSlock.acquire()
            for eventName in eventHandlerSockets:
                if self.request in eventHandlerSockets[eventName]:
                    print self.client_address,
                    print 'is no longer listening for event', eventName
                    eventHandlerSockets[eventName].remove(self.request)
        finally:
            eHSlock.release()

#end Class ECRequestHandler


#TODO: check for port number, print usage
#TODO: could have option to read port from 
# configuration file
port = int(sys.argv[1])


#TODO: can we or should we support other hostnames?
server = SocketServer.ThreadingTCPServer(
    ('localhost', port), ECRequestHandler)


#During load, print name
print "EventChat"
try:
    while 1:
        server.serve_forever()
except (KeyboardInterrupt, SystemExit):
    print "exiting on: ", sys.exc_info()[0]
###
# this should shutdown the server, but it doesn't, 
# so commenting it out
## server.shutdown()
###
    # let us at least exit on KeyboardInterrupt, SystemExit
    # only drawback, we often lose use of the current port for a time
    sys.exit()


