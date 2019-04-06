import numpy as np
from tqdm import tqdm
import cv2

def clear_data(seq, kernel_size=5):
    # Background should already be denoised under similar conditions
    padding = kernel_size//2
    padded_seq = np.concatenate((seq[padding:0:-1], seq, seq[-2:-2-padding:-1])).squeeze().astype(np.uint8)
    seq_copy = seq.copy()
    loop = tqdm(range(seq.shape[0]))
    for i in loop:
        frame = cv2.fastNlMeansDenoisingMulti(padded_seq, i+padding, kernel_size)
        seq_copy[i] = np.reshape(frame, seq_copy[i].shape)
    return seq_copy
