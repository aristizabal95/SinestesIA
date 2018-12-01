# THIS MODULE CONTAINS ALL THE LOGIC NECESSARY FOR READING/WRITING DATA WINTO HDF5 DATASETS
import h5py
import numpy as np

hdf5_path = 'raw_dataset.hdf5'
video_path = 'video'
actions_path = 'actions'
maxsize = 19200

def store_raw(timestamp, video, actions):
    f = h5py.File(hdf5_path, 'a')
    video_dir = video_path + '/' + timestamp
    if not video_dir in f:
        print("creating new file")
        f.create_dataset(video_dir, video.shape, maxshape=(maxsize, video.shape[1], video.shape[2], video.shape[3]), dtype=np.int8, chunks=True, data=video) # allow max 10 minutes
    else:
        f[video_dir].resize((f[video_dir].shape[0] + video.shape[0]), axis = 0)
        f[video_dir][-video.shape[0]:] = video
    # print("video saved")

    actions_dir = actions_path + '/' + timestamp
    if not actions_dir in f:
        f.create_dataset(actions_dir, actions.shape, maxshape=(maxsize, actions.shape[1]), dtype=np.float32, chunks=True, data=actions)
    else:
        f[actions_dir].resize((f[actions_dir].shape[0] + actions.shape[0]), axis = 0)
        f[actions_dir][-actions.shape[0]:] = actions
    # print("actions saved")

    f.close()

def combine_video_dataset():
    dset = h5py.File('video_dataset.hdf5', 'w')
    f = h5py.File(hdf5_path, 'r')
    for timestamp in list(f['video'].keys()):
        if not 'video' in dset:
            dset.create_dataset('video', f['video'][timestamp].shape, maxshape=(None,f['video'][timestamp].shape[1],f['video'][timestamp].shape[2],f['video'][timestamp].shape[3]),dtype=np.int8,chunks=True,data=f['video'][timestamp][:])
        else:
            dset['video'].resize((dset['video'].shape[0] + f['video'][timestamp].shape[0]), axis=0)
            dset['video'][-f['video'][timestamp].shape[0]:] = f['video'][timestamp][:]
