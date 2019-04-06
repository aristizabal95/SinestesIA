import h5py
import numpy as np
from PIL import Image

class CAEData:
    def __init__(self,config):
        self.config = config
        self.thresh = 8
        location = '/Volumes/TOSHIBA/TESIS/runtime/data/'
        f = h5py.File(location + 'video_dataset.hdf5','r')
        self.cv_input = f['test_data']
        self.input = f['train_data']
        im = Image.open(location + 'background.jpg')
        background = np.asarray(im)*self.config.background_percent
        self.background = np.reshape(background, self.config.state_size)

    def next_batch(self, batch_size):
        idx = np.random.choice(self.input.shape[0]-batch_size)
        batch_x = self.input[idx:idx+batch_size]
        batch_x = np.rollaxis(batch_x, 1, 4)
        # Remove background and normalize data
        batch_y = np.clip(((batch_x-self.background)-self.thresh)/(255-self.thresh), 0, 1)
        batch_x = batch_x/255
        noise = np.random.normal(0.5,0.5,((batch_size, 128, 128, 1)))
        noise_bool = np.random.normal(0,0.01,((batch_size,1,1,1)))
        batch_x = np.clip((batch_x + self.config.noise_percent*noise_bool*noise),0,1)
        yield batch_x, batch_y

    def cv_batch(self, batch_size=3):
        idx = np.random.choice(self.cv_input.shape[0]-batch_size)
        batch_x = self.cv_input[idx:idx+batch_size]
        batch_x = np.rollaxis(batch_x, 1, 4)
        batch_y = np.clip(((batch_x-self.background)-self.thresh)/(255-self.thresh), 0, 1)
        batch_x = batch_x/255
        yield batch_x, batch_y
