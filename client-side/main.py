import subprocess as sp
import numpy as np
import cv2
import face_recognition

FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
            '-srtp_in_suite', 'AES_CM_128_HMAC_SHA1_80',
            '-srtp_in_params', '00108310518720928b30d38f41149351559761969b71d79f8218a39259a7',
            '-i', 'srtp://192.168.0.101:1234',
            '-f', 'image2pipe',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'rgb24', '-']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
process_this = True

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
    small_image = cv2.resize(cv_image, (0,0), fx=0.5, fy=0.5)
    # from bgr to rgb
    small_image = small_image[:,:,::-1]

    # process every second frame for speeds sake
    if process_this:
        #Find all the faces. For now only positions, no encoding
        face_locations = face_recognition.face_locations(small_image)

    process_this = not process_this

    for (top,right, bottom, left) in face_locations:
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        # get the center of the face for positioning kinect
        y_pos = (top + bottom) / 2
        x_pos = (left + right) / 2

        cv2.rectangle(show_image, (right, bottom), (left, top), (0,0,255), 2)
        cv2.rectangle(show_image, (left, bottom - 35), (right, bottom), (0,0,255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(show_image, (str(x_pos - 640/2)+","+str(y_pos - 480/2)), (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)

    cv2.imshow('MONIKA', show_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

