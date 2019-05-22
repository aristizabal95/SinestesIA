from multiprocessing import Process
import subprocess as sp
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

import global_vars as global_vars
from data_man import *
from pure_data import *

recording = False
recording_count = 0
is_pressed = False
current_timestamp = ''

batch_size = 200
actions_size = 174
desired_fps = 44

video_buffer = np.zeros(shape=(batch_size,1,128,128))
video_storage = np.empty(shape=(batch_size,1,128,128))
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
                '-benchmark',
                '-i', 'udp://localhost:1234',
                '-f', 'image2pipe',
                '-vcodec', 'rawvideo',
                '-pix_fmt', 'gray', '-'
                ]
    pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)
    while True:
        raw_image = pipe.stdout.read(480*640)
        image = np.fromstring(raw_image, dtype='uint8')
        # OpenCV interprets images inverted
        # cv_image = image[0:480*640*3].reshape((480,640,3))
        depth_image = image.reshape((480,640))
        depth_image = np.flip(depth_image, 1)
        # cv_image = np.flip(cv_image, 1)
        # cv_image = np.dstack((cv_image, depth_image))
        depth = cv2.resize(depth_image, dsize=(128,128), interpolation=cv2.INTER_NEAREST)
        mask = np.abs(np.floor(depth/127).astype(bool).astype(np.uint8)-1)
        depth = depth*mask
        depth = (depth/127.0*255.0).astype(np.uint8)
        depth = cv2.GaussianBlur(depth, (5,5), 5)
        # cv_image = cv2.resize(cv_image, dsize=(128,128), interpolation=cv2.INTER_NEAREST)
        #with frame_lock:
        global_vars.g_current_frame = depth.astype(np.uint8).copy()

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

    show_image = global_vars.g_current_frame.astype(np.uint8).copy()
    cv2.namedWindow('SinestesIA', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('SinestesIA', 800,800)
    show_image = cv2.applyColorMap(show_image, cv2.COLORMAP_RAINBOW)
    cv2.imshow('SinestesIA', show_image)
    if(recording):
        # video_buffer[recording_count] = np.moveaxis(global_vars.g_current_frame, -1, 0) #TODO # creo que aquí se esta rotando la imagen
        video_buffer[recording_count] = global_vars.g_current_frame
        actions_buffer[recording_count] = np.array(global_vars.g_current_state)[:174]
        bar.update(recording_count + 1)
        if recording_count >= batch_size-1: #reached the end of the buffer, execute store callback and reset counter
            try:
                p = Process(target=store_raw, args=(current_timestamp,video_buffer,actions_buffer))
                p.start()
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
    if (elapsed < desired_elapsed):
        time.sleep(desired_elapsed - elapsed) #Sleep enough time to make each loop take the desired time
    end_time = time.time()
    fps = 1/(end_time - start_time)
    start_time = time.time()
