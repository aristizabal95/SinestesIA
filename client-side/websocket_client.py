from websocket import create_connection
import signal
import sys

die = False
def signal_handler(signal, frame):
    global die
    print('Killing connection')
    die = True

ws = create_connection("ws://192.168.0.101:8080")
while(not die):
    result = ws.recv()
    print("Received: '%s'" % result)
ws.close()
