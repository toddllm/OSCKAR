import socket

def readChunk(sock):
    chunk = ''
    lineLen = int(sock.recv(4))
    while lineLen > 0:
        chunk += sock.recv(lineLen)
        lineLen = int(sock.recv(4))
    return chunk


def makeChunk(s):
    chunk = ''
    while len(s) > 9999:
        chunk += "9999" + s[:9999]
        s = s[9999:]
    lengthString = ''
    if len(s) < 10:
        lengthString = "000" + str(len(s))
    elif len(s) < 100:
        lengthString = "00" + str(len(s))
    else:
        lengthString = "0" + str(len(s))
    chunk += lengthString + s + "0000"
    return chunk



import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', int(sys.argv[1])))
print 'connected on port',sys.argv[1]


print sys.argv[2]
sock.send(sys.argv[2])

print makeChunk(sys.argv[3])
sock.send(makeChunk(sys.argv[3]))

if len(sys.argv) > 3:
    print makeChunk(sys.argv[4])
    sock.send(makeChunk(sys.argv[4]))

sock.send('byebye')
