import tensorflow as tf
import numpy as np
import h5py
import utils.pure_data as pd

from models.rnn_model import RNNModel
from models.cae_xs_dropout import CAEModel
from utils.config import process_config
from utils.utils import get_args
import matplotlib.pyplot as plt

def load_models(c_c, r_c):
    # Load the models on separate sessions
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

    return cae, c_s, rnn, r_s

def predict(cae, c_s, rnn, r_s, action_arr, image_arr, state=np.zeros((2,2,1,1024))):
    # obtain the encoding of the input image
    encoding = c_s.run(cae.encoded, feed_dict={cae.x: image_arr})
    # concatenate action_arr with flattened encoding
    encoding = encoding.flatten().reshape((1,-1))
    rnn_input = np.concatenate((action_arr, encoding), axis=1)
    rnn_input = rnn_input.reshape((1,1,-1))
    # get the output and state of the rnn
    rnn_output, state = r_s.run([rnn.norm_pred, rnn.state], feed_dict={rnn.x: rnn_input, rnn.init_state: state})
    rnn_output = rnn_output.flatten().reshape((1,-1))
    actions_output = rnn_output[:,0:174]
    encoding_output = rnn_output[:,174:].reshape((1,2,2,4))
    # get decoded image
    decoded_output = c_s.run(cae.decoded, feed_dict={cae.encoded: encoding_output})
    return [actions_output, decoded_output, state, encoding_output]


def main():
    try:
        args = get_args()
        c_c = process_config(args.caeconfig)
        r_c = process_config(args.rnnconfig)

    except:
        print("Missing or invalid arguments")
        exit(0)

    f = h5py.File('data/sequences.hdf5')
    img = None
    sequences = f['video']
    sequence_no = np.random.randint(sequences.shape[0])
    # sequence = sequences[sequence_no]
    sequence = sequences[0]
    actions = np.zeros((1,174))
    state = np.zeros((2,2,1,1024))
    cae, c_s, rnn, r_s = load_models(c_c, r_c)
    for i in range(sequence.shape[0]):
        frame = np.rollaxis(sequence[[i]],1,4)
        real = np.copy(frame)
        actions, frame, state, _ = predict(cae, c_s, rnn, r_s, actions, frame, state)
        if img is None:
            img = plt.imshow(frame.squeeze())
        else:
            img.set_data(frame.squeeze())
        plt.pause(1/40000.0)
        plt.draw()
        msg = ' '.join(map(str, actions.squeeze()[:174])) + ';'
        pd.send2Pd(msg)

if __name__ == '__main__':
    main()
