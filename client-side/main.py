<<<<<<< HEAD
from data_man import *
import subprocess as sp
from pure_data import *
from socket import *
import numpy as np
import progressbar
import threading
import datetime
import keyboard
import time
import math
import h5py
import cv2

import global_vars


recording = False
recording_count = 0
is_pressed = False
current_timestamp = ''

batch_size = 200
actions_size = 174
desired_fps = 20

video_buffer = np.zeros(shape=(batch_size,4,240,320))
video_storage = np.empty(shape=(batch_size,4,240,320))
actions_buffer = np.zeros(shape=(batch_size,actions_size))
actions_storage= np.empty(shape=(batch_size,actions_size))

frame_lock = threading.Lock()

global_vars.init()

# Create the progressbar to display the batches of data being stored on RAM
bar = progressbar.ProgressBar(maxval=batch_size, widgets = [progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

def getVideoData():
    global frame_lock
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
    while True:
        raw_image = pipe.stdout.read(480*640*4)
        image = np.fromstring(raw_image, dtype='uint8')

        # OpenCV interprets images inverted
        cv_image = image[0:480*640*3].reshape((480,640,3))
        depth_image = image[(480*640*3):].reshape((480,640))
        depth_image = np.flip(depth_image, 1)
        cv_image = np.flip(cv_image, 1)
        cv_image = np.dstack((cv_image, depth_image))
        cv_image = cv2.resize(cv_image, dsize=(320,240), interpolation=cv2.INTER_NEAREST)
        #with frame_lock:
        global_vars.g_current_frame = cv_image.astype(np.uint8).copy()

# Create the video stream thread
try:
    t = threading.Thread(target=getVideoData)
    t.start()
except:
    print("Something went wrong trying to start getVideoData")
# Create the pure data receive thread
try:
    t = threading.Thread(target=pdreceive)
    t.start()
except:
    print("Something went wrong trying to start pdreceive")

start_time = time.time()
while(True):
    if keyboard.is_pressed('space'):
        is_pressed = True
    else:
        if is_pressed:
            recording = not recording
            if recording:
                current_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime("%Y_%m_%d_%H_%M_%S")
                recording_count = 0
                print("Recording on dataset " + str(current_timestamp))
                bar.start()
            is_pressed = False
        
    #with frame_lock:
    show_image = global_vars.g_current_frame.astype(np.uint8).copy()

    cv2.imshow('ImprovAI', show_image)
    if(recording):
        video_buffer[recording_count] = np.moveaxis(global_vars.g_current_frame, -1, 0)
        actions_buffer[recording_count] = np.array(global_vars.g_current_state)[:174]
        bar.update(recording_count + 1)
        if recording_count >= 199: #reached the end of the buffer, execute store callback and reset counter
            video_storage = np.copy(video_buffer)
            actions_storage = np.copy(actions_buffer)
            try:
                t = threading.Thread(target=store_raw, args=(current_timestamp,video_storage,actions_storage))
                t.start()
            except:
                print("Could not create storage thread!!!!")
            recording_count = 0
            bar.finish()
            bar.start()
        recording_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # measure time
    end_time = time.time()
    elapsed = end_time - start_time
    desired_elapsed = 1/desired_fps
    if (elapsed > desired_elapsed):
        print("Process is running slower than desired! Check your fps limit and lower it.")
    else:
        time.sleep(desired_elapsed - elapsed) #Sleep enough time to make each loop take the desired time
    end_time = time.time()
    fps = 1/(end_time - start_time)
    print("fps: " + str(fps))
    start_time = time.time()
=======
import subprocess as sp
import numpy as np
import cv2
# import face_recognition
from socket import *
import math


FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
            '-loglevel', 'quiet',
            '-srtp_in_suite', 'AES_CM_128_HMAC_SHA1_80',
            '-srtp_in_params', '00108310518720928b30d38f41149351559761969b71d79f8218a39259a7',
            '-i', 'srtp://localhost:1234',
            '-f', 'image2pipe',
            '-vcodec', 'rawvideo',
            '-pix_fmt', 'rgb24', '-'
            ]
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
process_this = True
start_move_count = 0
y_dist_array = []
x_dist_array = []
div_epsilon = 0.0000001
cmd = 0b000000000000000000000000
current_tilt = 0
current_yaw = 0

# def generateCommand(idle, fmt, tilt, yaw, led, brightness):
#     byte1 = 0
#     byte2 = 0
#     byte3 = 0
# 
#     # The inputs are received in their original meaning. Therefore, some ranges need to be transformed
#     # Ensure tilt is between -30 and 30
#     tilt = sorted((-30, tilt, 30))[1]
#     # Normalize to 0,60
#     tilt += 30
# 
#     # Ensure yaw is betwee -90 and 90
#     yaw = sorted((-90, yaw, 90))[1]
#     # Normalize to 0,180
#     yaw += 90
#     
#     # Build the message inverting the order of each variable on the byte
#     byte1 += tilt
#     # Shift to leave space for idle and fmt
#     byte1 = byte1 << 2
#     # Add fmt to the second position of byte
#     byte1 += 2*fmt
#     # Add idle to the first position of byte
#     byte1 += idle
#     byte2 = yaw
#     byte3 += brightness
#     byte3 = byte3 << 3
#     byte3 += led
#     cmd = byte1.to_bytes(1, byteorder='little') + byte2.to_bytes(1, byteorder="little") + byte3.to_bytes(1, byteorder="little") 
#     return cmd, (tilt - 30), (yaw - 90)

# s = socket(AF_INET, SOCK_STREAM)
# s.connect(("192.168.0.101", 6666))

while(True):
    raw_image = pipe.stdout.read(480*640*3*2)
    image = np.fromstring(raw_image, dtype='uint8')

    # OpenCV interprets images inverted
    cv_image = image[0:480*640*3].reshape((480,640,3))
    depth_image = image[(480*640*3):].reshape((480,640,3))
    depth_image = np.flip(depth_image, 1)
    cv_image = np.flip(cv_image, 1)

    # Also need to invert the order of colors
    cv_image = cv_image[...,::-1]
    # depth_image = depth_image[...,::-1]
    # image = np.swapaxes(image, 0, 1)
    show_image = cv_image.astype(np.uint8).copy()
    # show_image = depth_image.astype(np.uint8).copy()

    # resize for fast face recognition
    # little_image = cv2.resize(cv_image, (0,0), fx=0.5, fy=0.5)
    # from bgr to rgb
    # little_image = little_image[:,:,::-1]

    # process every second frame for speeds sake
    # if process_this:
        #Find all the faces. For now only positions, no encoding
    #    face_locations = face_recognition.face_locations(little_image)

    # process_this = not process_this
    # x_dist = 0
    # y_dist = 0

    # for (top,right, bottom, left) in face_locations:
    #     top *= 2
    #     right *= 2
    #     bottom *= 2
    #     left *= 2

    #     # get the center of the face for positioning kinect
    #     y_pos = (top + bottom) / 2
    #     x_pos = (left + right) / 2
    #     x_dist = (x_pos - 640/2)/4
    #     y_dist = -(y_pos - 480/2)/4

    #     cv2.rectangle(show_image, (right, bottom), (left, top), (0,0,255), 2)
    #     cv2.rectangle(show_image, (left, bottom - 35), (right, bottom), (0,0,255), cv2.FILLED)
    #     font = cv2.FONT_HERSHEY_DUPLEX
    #     cv2.putText(show_image, (str(x_dist)+","+str(y_dist)), (left + 6, bottom - 6), font, 1.0, (255,255,255), 1)

    cv2.imshow('MONIKA', show_image)
    # if not face_locations:
    #     led = 2
    # else:
    #     led = 1

    # if start_move_count == 3:
    #     y_mean_dist = sum(y_dist_array) /3.0
    #     x_mean_dist = sum(x_dist_array) /3.0
    #     y_mean_dist = math.tanh(abs(y_dist))*math.tanh(y_mean_dist/3)*3
    #     x_mean_dist = math.tanh(abs(x_dist))*math.tanh(x_mean_dist/3)*3
    #     y_dist_array = []
    #     x_dist_array = []
    #     cmd, current_tilt, current_yaw = generateCommand(1, 1, current_tilt + int(y_mean_dist), current_yaw + int(x_mean_dist), led, 0)
    #     sent = s.send(cmd)
    #     if sent == 0:
    #         raise RuntimeError("Socket connection broken")
    #     start_move_count = 0
    # else:
    #     y_dist_array.append(y_dist)
    #     x_dist_array.append(x_dist)
    # start_move_count += 1


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
>>>>>>> 5cb2ae6be3519fc789be6a8f7d8f7e21a10ff960

