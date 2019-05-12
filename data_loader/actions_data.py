import h5py
import numpy as np

class ActionsData:
    def __init__(self,config):
        self.config = config
        location = 'E:/Alejandro/Tesis/data/'
        f = h5py.File(location + 'rnn.hdf5','r')
        self.cv_input = f['test_data']
        self.input = f['train_data']
        self.cv_output = f['test_labels']
        self.output = f['train_labels']

    def next_batch(self, batch_size):
        idx = np.random.randint(self.input.shape[0]-batch_size)
        batch_x = self.input[idx:idx+batch_size]
        batch_y = self.output[idx:idx+batch_size]
        yield batch_x, batch_y

    def cv_batch(self, batch_size=3):
        idx = np.random.randint(self.cv_input.shape[0]-batch_size)
        batch_x = self.cv_input[idx:idx+batch_size]
        batch_y = self.cv_output[idx:idx+batch_size]
        yield batch_x, batch_y

    def get_mean(self):
        return np.mean(self.cv_input[:], axis=0)

    def get_stdev(self):
        data = self.cv_input[:]
        return data.max(0) - data.min(0)
