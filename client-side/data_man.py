# THIS MODULE CONTAINS ALL THE LOGIC NECESSARY FOR READING/WRITING DATA WINTO HDF5 DATASETS
import h5py
import numpy as np

hdf5_path = 'raw_dataset.hdf5'
video_path = 'video'
actions_path = 'actions'

def store_raw(timestamp, video, actions):
    f = h5py.File(hdf5_path, 'a')
    print(video)
    print(actions)
    video_dir = video_path + '/' + timestamp
    if not video_dir in f:
        f.create_dataset(video_dir, video.shape, maxshape=(4800, video.shape[1], video.shape[2], video.shape[3]), dtype=np.int8, chunks=True, data=video) # allow max 10 minutes
    else:
        f[video_dir].resize((f[video_dir].shape[0] + video.shape[0]), axis = 0)
        f[video_dir][-video.shape[0]:] = video
    print("video saved")

    actions_dir = actions_path + '/' + timestamp
    if not actions_dir in f:
        f.create_dataset(actions_dir, actions.shape, maxshape=(4800, actions.shape[1]), dtype=np.float32, chunks=True, data=actions)
    else:
        f[actions_dir].resize((f[actions_dir].shape[0] + actions.shape[0]), axis = 0)
        f[actions_dir][-actions.shape[0]:] = actions
    print("actions saved")

    f.close()
