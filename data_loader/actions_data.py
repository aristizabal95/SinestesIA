import h5py
import numpy as np

class ActionsData:
    def __init__(self,config):
        self.config = config
        f = h5py.File('data/rnn_outputs.hdf5','r')
        self.input = f['rnn']
        self.output = f['actions']

    def next_batch(self, batch_size):
        idx = np.random.randint(self.input.shape[0]-batch_size)
        batch_x = self.input[idx:idx+batch_size]
        batch_y = self.output[idx:idx+batch_size]
        yield batch_x, batch_y

    def cv_batch(self, batch_size=3):
        idx = np.random.choice(self.cv_input.shape[0], batch_size)
        yield self.cv_input[idx], self.cv_y[idx]
