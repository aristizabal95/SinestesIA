import h5py
import numpy as np
from models.cae_l_high import CAEModel
from utils.config import process_config
import tensorflow as tf

class RNNData:
    def __init__(self,config):
        self.config = config
        self.index = 0
        f = h5py.File('data/sequences.hdf5','r')
        self.video = f['video']
        self.cae_g = tf.Graph()
        self.sess = tf.Session(graph=self.cae_g)
        cae_config = process_config('configs/cae_l_high_receptive_field.json')
        with self.cae_g.as_default():
            self.model = CAEModel(cae_config)
        with self.sess.as_default():
            with self.cae_g.as_default():
                self.model.load(self.sess)

    def next_batch(self):
        index = self.index
        time_slices = np.floor(self.video.shape[1] / (self.config.timesteps+1))
        current_time_slice = index % time_slices
        start_idx = int(self.config.timesteps*current_time_slice)
        end_idx = int(start_idx + self.config.timesteps + 1)
        video_dataset = self.video[:,start_idx:end_idx,:,:,:]
        video_dataset = np.rollaxis(video_dataset,2,5)
        # Resize batch for cae processing
        video_batch = video_dataset.reshape(-1,128,128,1)
        encoded_batch = self.sess.run(self.model.encoded, feed_dict={self.model.x: video_batch})
        encoded_batch = np.reshape(encoded_batch, [self.video.shape[0], self.config.timesteps+1, -1])
        batch = encoded_batch
        batch_x = batch[:,0:-1,:]
        batch_y = batch[:,1:,:]
        self.index = self.index + 1
        yield current_time_slice, batch_x, batch_y

    def cv_batch(self, batch_size=3):
        idx = np.random.choice(self.cv_input.shape[0], batch_size)
        yield self.cv_input[idx], self.cv_y[idx]
