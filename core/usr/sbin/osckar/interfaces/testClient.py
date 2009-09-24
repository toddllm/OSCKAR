#!/usr/bin/python -Wall

import sys
sys.path.append('/usr/local/share/osckar/lib/')
import comm as c
import socket

#hardcode SERVER to localhost for testing locally
SERVER = "localhost"

class testClient:

    def __init__(self, port):
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.comm = c.Comm()

    def connect(self, server):
        self.sock.connect((server, self.port))

    def send(self, toSend):
        self.sock.send(toSend)

#end Class testClient


#main
print "testClient"

port = int(sys.argv[1])
myClient = testClient(port)
myClient.connect(SERVER)

while 1:
    userInput = sys.stdin.readline()
    myClient.send(userInput)
