# import pure_data as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt

def replay_data(video,actions):
    img = None
    video = np.rollaxis(video[:],1,4)
    for i in range(video.shape[0]):
        frame = video[i]
        if img is None:
            img = plt.imshow(np.squeeze(frame))
        else:
            img.set_data(np.squeeze(frame))
        plt.pause(.0025)
        plt.draw()

        msg = ' '.join(map(str, actions[i])) + ';'
        pd.send2Pd(msg)
    print("Done!")

def display_video(video_array, time=0.01):
    # Receives an array of images to display and optionally the time between frames
    # Displays the video
    img = None
    for i in range(video_array.shape[0]):
        frame = video_array[i]
        if img is None:
            img = plt.imshow(np.squeeze(frame))
        else:
            img.set_data(np.squeeze(frame))
        plt.pause(.0025)
        plt.draw()

def display_clean_video(video_array, time=0.01):
    # Receives an array of images to display and optionally the time between frames
    # Displays the video
    img = None
    fgbg = cv2.createBackgroundSubtractorMOG2()
    for i in range(video_array.shape[0]):
        frame = video_array[i].squeeze()
        frame = fgbg.apply(frame)
        if img is None:
            img = plt.imshow(np.squeeze(frame))
        else:
            img.set_data(np.squeeze(frame))
        plt.pause(.0025)
        plt.draw()

def display_sequence(frame, sequence):
    # Receives a numpy array representing an image, and
    # a plt.imshow() object representing the display to update
    if sequence is None:
        sequence = plt.imshow(frame)
    else:
        sequence.set_data(frame)
    plt.pause(.0025)
    plt.draw()
    return sequence
