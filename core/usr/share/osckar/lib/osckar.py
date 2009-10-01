#!/usr/bin/python

import sys
sys.path.append('/usr/local/share/osckar/lib/')
import comm as c
import socket

comm = c.Comm()

class Osckar:

    def __init__(self):
        return

    def connect(self,host,port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('localhost', int(port)))
                          
    def signal(self,name,args):
        self.sock.send('signal' + comm.makeChunk(name) + comm.makeChunk(args))

    def registerEvent(self,name):
        self.sock.send('regevt' + comm.makeChunk(name))

    def registerEvents(self,names):
        for name in names:
            registerEvent(name)

    def waitForEvent(self,name):
        while True:
            procedure = self.sock.recv(6)
            if procedure == 'signal':
                eventName = comm.readChunk(self.sock)
                eventArgs = comm.readChunk(self.sock)
                if eventName == name:
                    return eventArgs # return event's arguments

    def waitForEvents(self,names):
        while True:
            procedure = self.sock.recv(6)
            if procedure == 'signal':
                eventName = comm.readChunk(self.sock)
                eventArgs = comm.readChunk(self.sock)
                for name in names:
                    if eventName == name:
                        return [name,eventArgs] # return event's name and args

