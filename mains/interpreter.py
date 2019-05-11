from multiprocessing import Process
import subprocess as sp
import tensorflow as tf
import utils.pure_data as pd
from models.dance_rnn_model import RNNModel
from models.cae_l_high import CAEModel
from models.actions_model import ActionsModel
from utils.config import process_config
from utils.utils import get_args
from socket import *
import numpy as np
import threading
import time
import math
import cv2

class Interpreter:
    # ATTRIBUTES
    # self.current_frame = None

    def __init__(self, cc_path='configs/cae_remade.json', rc_path='configs/dance_rnn_prod.json', ac_path='configs/actions_config.json'):
        # Here comes all the initialization required
        # Initialize the models
        self.cc = process_config(cc_path)
        self.rc = process_config(rc_path)
        self.ac = process_config(ac_path)
        self.cae, self.c_s, self.rnn, self.r_s, self.actions, self.a_s = self.load_models(self.cc, self.rc, self.ac)
        self.current_frame = np.zeros((128,128))
        # Create the video stream thread
        try:
            t = threading.Thread(target=self.getVideoData)
            t.start()
            print("thread started")
        except:
            print("Something went wrong trying to start getVideoData")
            # Create the pure data receive thread

    def getVideoData(self):
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
            depth_image = image.reshape((480,640))
            depth_image = np.flip(depth_image, 1)
            depth = cv2.resize(depth_image, dsize=(128,128), interpolation=cv2.INTER_NEAREST)
            mask = np.abs(np.floor(depth/127).astype(bool).astype(np.uint8)-1)
            depth = depth*mask
            depth = (depth/127.0*255.0).astype(np.uint8)
            depth = cv2.GaussianBlur(depth, (5,5), 5)
            #with frame_lock:
            self.current_frame = depth.astype(np.uint8).copy()

    def load_models(self, c_c, r_c, a_c):
        # Load the models on separate sessions
        print("Loading the models")
        c_g = tf.Graph()
        with c_g.as_default():
            cae = CAEModel(c_c)

        c_s = tf.Session(graph=c_g)
        with c_s.as_default():
            with c_g.as_default():
                cae.load(c_s)

        r_g = tf.Graph()
        with r_g.as_default():
            rnn = RNNModel(r_c)

        r_s = tf.Session(graph=r_g)
        with r_s.as_default():
            with r_g.as_default():
                rnn.load(r_s)

        a_g = tf.Graph()
        with a_g.as_default():
            actions = ActionsModel(a_c)

        a_s = tf.Session(graph=a_g)
        with a_s.as_default():
            with a_g.as_default():
                actions.load(a_s)

        return cae, c_s, rnn, r_s, actions, a_s

    def run(self):
        init_state = np.zeros((self.rc.lstm_layers,2,self.rc.batch_size,self.rc.hidden_size))
        img = None
        while True:
            image = self.current_frame.reshape((1,128,128,1))
            encoding = self.c_s.run(self.cae.encoded, feed_dict={self.cae.x: image/255*0.6})
            encoding = encoding.reshape((1, 1,-1))
            prediction, init_state = self.r_s.run([self.rnn.norm_pred, self.rnn.state], feed_dict={self.rnn.x: encoding, self.rnn.init_state: init_state})
            encoded = prediction.reshape((1,1,1,-1))
            decoded = self.c_s.run(self.cae.decoded, feed_dict={self.cae.encoded: encoded})
            encoded = encoded.reshape((8,4,4))
            encoded = cv2.resize(encoded/encoded.max(), (500,500))
            decoded = cv2.resize(decoded.squeeze()/decoded.max(), (500,500))
            decoded = np.stack((decoded,)*3)
            decoded = np.vstack((decoded, np.ones((1,500,500))))
            decoded = np.rollaxis(decoded, 0, 3)
            show_img = np.concatenate((encoded, decoded), axis=1)
            cv2.imshow('perform', show_img)
            cv2.waitKey(1)
            actions = self.a_s.run(self.actions.prediction, feed_dict={self.actions.x: np.asarray(init_state).reshape((1,-1))})
            msg = ' '.join(map(str, actions.squeeze())) + ';'
            pd.send2Pd(msg)

if __name__ == '__main__':
    i = Interpreter()
    i.run()
