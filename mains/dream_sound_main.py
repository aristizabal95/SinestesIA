import tensorflow as tf
import numpy as np
import utils.pure_data as pd

from models.dance_rnn_model import RNNModel
from models.cae_xs_dropout import CAEModel
from models.actions_model import ActionsModel
from utils.config import process_config
from utils.utils import get_args
import matplotlib.pyplot as plt

def load_models(c_c, r_c, a_c):
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

    a_g = tf.Graph()
    with a_g.as_default():
        actions = ActionsModel(a_c)

    a_s = tf.Session(graph=a_g)
    with a_s.as_default():
        with a_g.as_default():
            actions.load(a_s)

    return cae, c_s, rnn, r_s, actions, a_s

def dream(cae, c_s, rnn, r_s, actions, a_s, pred=np.zeros((1,1,16)), state=np.zeros((2,2,1,256)), length=300, randomize=True):
    img = None
    prediction = np.copy(pred)
    init_state = np.copy(state)
    print("Dreaming")
    while True:
        for _ in range(length):
            prediction, output, init_state = r_s.run([rnn.norm_pred, rnn.output, rnn.state], feed_dict={rnn.x: prediction, rnn.init_state: init_state})
            # init_state = init_state + np.random.rand(2,2,1,1024)*1.8
            encoded = prediction.squeeze().reshape((1,2,2,4))
            decoded = c_s.run(cae.decoded, feed_dict={cae.encoded: encoded})
            if img is None:
                img = plt.imshow(decoded.squeeze())
            else:
                img.set_data(decoded.squeeze())
            plt.pause(1/40.0)
            plt.draw()
            output = output.reshape((-1, 256))
            actions_arr = a_s.run(actions.norm_pred, feed_dict={actions.x: output})
            msg = ' '.join(map(str, actions_arr.squeeze())) + ';'
            pd.send2Pd(msg)
        if randomize:
            prediction = np.random.rand(1,1,16)*10
            init_state = np.random.rand(2,2,1,256)*100

def main():
    try:
        args = get_args()
        c_c = process_config(args.caeconfig)
        r_c = process_config(args.rnnconfig)
        a_c = process_config(args.actionsconfig)
        length = int(args.length)

    except:
        print("Missing or invalid arguments")
        exit(0)

    cae, c_s, rnn, r_s, actions, a_s = load_models(c_c, r_c, a_c)
    print(actions)
    pred = np.random.rand(1,1,16)*0.3
    state = np.random.rand(2,2,1,256)*100
    dream(cae,c_s,rnn,r_s,actions,a_s,pred,state,length)

if __name__ == '__main__':
    main()
