from base.base_model import BaseModel
import tensorflow as tf
import numpy as np

class RNNModel(BaseModel):
    def __init__(self,config):
        super(RNNModel,self).__init__(config)
        self.build_model()
        self.init_saver()

    def lstm_cell(self, hidden_size):
        lstm = tf.nn.rnn_cell.LSTMCell(hidden_size, forget_bias=1.0)
        return lstm

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool, name="training")
        # inst_max = [127, 1, 8000, 1, 1, 8000, 1, 50000, 1, 8000, 1, 1, 1, 20000, 4, 50000, 20, 50000, 4, 5, 20000, 20000, 20000, 1, 1, 1, 1, 1, 1]
        # inst_mean = [63.5, 0.5, 4000, 0.5, 0.5, 4000, 0.5, 25000, 0.5, 4000, 0.5, 0.5 , 0.5, 10000, 2, 25000, 10, 25000, 2, 2.5, 10000, 10000, 10000, 0.5, 0.5, 0.5, 0.5, 0.5, 0]
        enc_max = np.array([32.72663116455078,8.7772855758667,81.73662567138672,46.63551712036133,30.93536949157715,0.9027136564254761,66.04371643066406,67.35106658935547,36.75901412963867,11.51897144317627,51.02521896362305,46.63236618041992,33.83308410644531,19.863624572753906,72.692626953125,43.59470748901367])
        enc_mean = np.array([4.461085319519043,-9.29656982421875,14.543147087097168,2.361961603164673,6.676889419555664,-12.098401069641113,24.03343391418457,9.336644172668457,5.314021110534668,-7.672455787658691,7.461145401000977,8.348762512207031,2.163285493850708,-2.1502020359039307,9.220654487609863,3.469447374343872])
        # self.max = np.concatenate((np.tile(inst_max, 6),enc_max))
        self.max = enc_max
        # self.mean = np.concatenate((np.tile(inst_mean, 6),enc_mean))
        self.mean = enc_mean

        self.x = tf.placeholder(tf.float32, shape=[None, None] + self.config.state_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None, None] + self.config.state_size, name="Y")
        self.batch_size = tf.placeholder(tf.int32, shape=[])

        # Make the network infraestructure here
        # First normalize the input and labels
        norm_x = (self.x - self.mean)/(self.max - self.mean)

        # Setting up initial state to all zeros
        self.init_state = tf.placeholder(tf.float32, [self.config.lstm_layers, 2, self.config.batch_size, self.config.hidden_size])
        if self.config.lstm_layers > 1:
            state_per_layer_list = tf.unstack(self.init_state, axis=0)
        else:
            state_per_layer_list = self.init_state
        rnn_tuple_state = tuple(
            [tf.nn.rnn_cell.LSTMStateTuple(state_per_layer_list[idx][0], state_per_layer_list[idx][1])
            for idx in range(self.config.lstm_layers)]
        )

        # Stacking up the layers for deep learning
        cell = tf.nn.rnn_cell.MultiRNNCell([self.lstm_cell(self.config.hidden_size) for _ in range(self.config.lstm_layers)], state_is_tuple=True)

        output, self.state = tf.nn.dynamic_rnn(cell, norm_x, initial_state=rnn_tuple_state)
        self.output = output

        # Pass the output through a fully connected layer and get the predictions
        l1 = tf.contrib.layers.fully_connected(output, 128, activation_fn=tf.nn.sigmoid)
        logits = tf.contrib.layers.fully_connected(l1, self.config.state_size[0], activation_fn=None)
        # compress the results into values between -1 and 1
        self.prediction = tf.tanh(logits)
        self.norm_pred = self.prediction*(self.max - self.mean) + self.mean





        with tf.name_scope("loss"):
            loss = tf.losses.huber_loss(labels=((self.y-self.mean)/(self.max - self.mean)), predictions=self.prediction)
            reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
            self.cross_entropy = tf.reduce_mean(loss) + self.config.reg_constant*sum(reg_losses)
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy, global_step=self.global_step_tensor)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
