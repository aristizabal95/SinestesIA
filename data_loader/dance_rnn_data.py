import h5py
import numpy as np
from utils.config import process_config
import tensorflow as tf

class RNNData:
    def __init__(self,config):
        self.config = config
        self.index = 0
        self.seq_index = 0
        f = h5py.File('data/sequences.hdf5','r')
        self.video = f['sequences']

    def next_batch(self):
        index = self.index
        time_slices = np.floor(self.video.shape[1] / (self.config.timesteps+1))
        current_time_slice = index % time_slices
        if current_time_slice == 0:
            # If the batch has been fully analized, then change batch
            self.seq_index = np.random.randint(self.video.shape[0]-self.config.batch_size)
            self.index = 0

        start_idx = int(self.config.timesteps*current_time_slice)
        end_idx = int(start_idx + self.config.timesteps + 1)
        video_dataset = self.video[self.seq_index:self.seq_index+self.config.batch_size,start_idx:end_idx,:]
        batch = video_dataset
        batch_x = batch[:,0:-1,:]
        batch_y = batch[:,1:,:]
        self.index = self.index + 1
        yield current_time_slice, batch_x, batch_y

    def cv_batch(self, batch_size=3):
        idx = np.random.choice(self.cv_input.shape[0], batch_size)
        yield self.cv_input[idx], self.cv_y[idx]
