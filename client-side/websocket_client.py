from websocket import create_connection
import signal
import sys
import numpy as np
from PIL import Image

def signal_handler(signal, frame):
    global die
    print('Killing connection')
    die = True

ws = create_connection("ws://192.168.0.101:8080")
while(True):
    result = ws.recv()
    # print("Received: '%s'" % result)
    data = np.frombuffer(result, dtype=np.uint8)
    data = np.reshape(data, (480, 640, 3))
    img_data = np.swapaxes(data, 0, 1)
    im = Image.fromarray(img_data).transpose(Image.ROTATE_270)
    im.save('rgb.jpg')
    im.show()
    print(data.shape)
ws.close()
