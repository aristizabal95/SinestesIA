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
        self.mean = tf.get_variable("mean", shape=([128]), trainable=False)
        self.stdev = tf.get_variable("stdev", shape=([128]), trainable=False)

        self.x = tf.placeholder(tf.float32, shape=[None, None] + self.config.state_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None, None] + self.config.state_size, name="Y")
        self.batch_size = tf.placeholder(tf.int32, shape=[])

        # Make the network infraestructure here
        # First normalize the input and labels
        norm_x = (self.x - self.mean)/self.stdev

        # Start with a densely connected layer
        layer1 = tf.contrib.layers.fully_connected(norm_x, 256, activation_fn=tf.nn.relu)

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

        output, self.state = tf.nn.dynamic_rnn(cell, layer1, initial_state=rnn_tuple_state)
        self.output = output

        # Pass the output through a fully connected layer and get the predictions
        layer2 = tf.contrib.layers.fully_connected(output, 256, activation_fn=tf.nn.relu)
        self.norm_pred = tf.contrib.layers.fully_connected(layer2, self.config.state_size[0], activation_fn=tf.nn.relu)
        # compress the results into values between -1 and 1
        # self.prediction = tf.tanh(logits)
        # self.norm_pred = self.prediction*(self.max - self.mean) + self.mean
        self.prediction = self.norm_pred*self.stdev + self.mean





        with tf.name_scope("loss"):
            loss = tf.losses.huber_loss(labels=(self.y), predictions=self.prediction)
            # loss = tf.losses.mean_squared_error(labels=(self.y), predictions=self.prediction)
            reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
            self.cross_entropy = tf.reduce_mean(loss) + self.config.reg_constant*sum(reg_losses)
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy, global_step=self.global_step_tensor)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
