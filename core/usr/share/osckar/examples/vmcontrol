#!/usr/bin/python -Wall

import socket
import sys
sys.path.append('/usr/local/share/osckar/lib/')
import comm as c
comm = c.Comm()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', int(sys.argv[1])))
print 'connected on port',sys.argv[1]

output = ""

if sys.argv[2] == 'start':
    output = 'signal' + comm.makeChunk('START_VM')
    output += comm.makeChunk(sys.argv[3])
elif sys.argv[2] == 'shutdown':
    output = 'signal' + comm.makeChunk('SHUTDOWN_VM')
    output += comm.makeChunk(sys.argv[3])
elif sys.argv[2] == 'destroy':
    output = 'signal' + comm.makeChunk('DESTROY_VM')
    output += comm.makeChunk(sys.argv[3])
elif sys.argv[2] == 'import_vmc':
    output = 'signal' + comm.makeChunk('IMPORT_VMC')
    inFile = open(sys.argv[3],'r')
    output += comm.makeChunk(inFile.read())
    print output
    inFile.close()
else:
    sock.close()
    exit

sock.send(output)
sock.close()
