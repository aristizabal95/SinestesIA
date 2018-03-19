import subprocess as sp
import numpy as np
import cv2
import face_recognition
from socket import *


FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
            '-loglevel', 'quiet',
            '-srtp_in_suite', 'AES_CM_128_HMAC_SHA1_80',
            '-srtp_in_params', '00108310518720928b30d38f41149351559761969b71d79f8218a39259a7',
            '-i', 'srtp://192.168.0.101:1234',
            '-f', 'image2pipe',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'rgb24', '-'
            ]
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
process_this = True
cmd = 0b000000000000000000000000
current_tilt = 0
current_yaw = 0

def generateCommand(idle, fmt, tilt, yaw, led, brightness):
    byte1 = 0
    byte2 = 0
    byte3 = 0

    # The inputs are received in their original meaning. Therefore, some ranges need to be transformed
    # Ensure tilt is between -30 and 30
    tilt = sorted((-30, tilt, 30))[1]
    # Normalize to 0,60
    tilt += 30

    # Ensure yaw is betwee -90 and 90
    yaw = sorted((-90, yaw, 90))[1]
    # Normalize to 0,180
    yaw += 90
    
    # Build the message inverting the order of each variable on the byte
    byte1 += tilt
    # Shift to leave space for idle and fmt
    byte1 = byte1 << 2
    # Add fmt to the second position of byte
    byte1 += 2*fmt
    # Add idle to the first position of byte
    byte1 += idle
    byte2 = yaw
    byte3 += brightness
    byte3 = byte3 << 3
    byte3 += led
    cmd = byte1.to_bytes(1, byteorder='little') + byte2.to_bytes(1, byteorder="little") + byte3.to_bytes(1, byteorder="little") 
    return cmd, (tilt - 30), (yaw - 90)

s = socket(AF_INET, SOCK_STREAM)
s.connect(("192.168.0.101", 6666))

while(True):
    raw_image = pipe.stdout.read(480*640*3)
    image = np.fromstring(raw_image, dtype='uint8')

    # OpenCV interprets images inverted
    cv_image = image.reshape((480,640,3))
    cv_image = np.flip(cv_image, 1)

    # Also need to invert the order of colors
    cv_image = cv_image[...,::-1]
    # image = np.swapaxes(image, 0, 1)
    show_image = cv_image.astype(np.uint8).copy()

    # resize for fast face recognition
    little_image = cv2.resize(cv_image, (0,0), fx=0.5, fy=0.5)
    # from bgr to rgb
    little_image = little_image[:,:,::-1]

    # process every second frame for speeds sake
    if process_this:
        #Find all the faces. For now only positions, no encoding
        face_locations = face_recognition.face_locations(little_image)

    process_this = not process_this
    x_dist = 0
    y_dist = 0

    for (top,right, bottom, left) in face_locations:
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # get the center of the face for positioning kinect
        y_pos = (top + bottom) / 2
        x_pos = (left + right) / 2
        x_dist = (x_pos - 640/2)/10
        y_dist = -(y_pos - 480/2)/10

        cv2.rectangle(show_image, (right, bottom), (left, top), (0,0,255), 2)
        cv2.rectangle(show_image, (left, bottom - 35), (right, bottom), (0,0,255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(show_image, (str(x_dist)+","+str(y_dist)), (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)

    cv2.imshow('MONIKA', show_image)

    if process_this:
        cmd, current_tilt, current_yaw = generateCommand(1, 1, current_tilt + int(y_dist), current_yaw + int(x_dist), 1, 0)
        sent = s.send(cmd)
        if sent == 0:
            raise RuntimeError("Socket connection broken")


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

