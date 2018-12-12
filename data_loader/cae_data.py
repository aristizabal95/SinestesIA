import h5py
import numpy as np

class CAEData:
    def __init__(self,config):
        self.config = config
        f = h5py.File('data/dataset.hdf5','r')
        data = np.rollaxis(f['train_data'][:],1,4)
        data = data/data.max()
        labels = np.rollaxis(f['train_labels'][:],1,4)
        cv_data = np.rollaxis(f['cross_val_data'][:],1,4)
        cv_labels = np.rollaxis(f['cross_val_labels'][:],1,4)
        self.cv_input = cv_data
        self.cv_y = cv_labels
        self.input = data
        self.y = labels

    def next_batch(self, batch_size):
        idx = np.random.choice(self.input.shape[0], batch_size)
        batch_x = self.input[idx]
        noise = np.random.normal(0.5,0.5,((batch_size, 128, 128, 1)))
        noise_bool = np.random.normal(0,0.01,((batch_size,1,1,1)))
        batch_x = np.clip((batch_x + self.config.noise_percent*noise_bool*noise),0,1)
        yield batch_x, self.y[idx]

    def cv_batch(self, batch_size=3):
        idx = np.random.choice(self.cv_input.shape[0], batch_size)
        yield self.cv_input[idx], self.cv_y[idx]
