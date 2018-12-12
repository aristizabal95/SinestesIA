from base.base_model import BaseModel
import tensorflow as tf

class RNNModel(BaseModel):
    def __init__(self,config):
        super(RNNModel,self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool, name="training")

        self.x = tf.placeholder(tf.float32, shape=[None, self.config.timesteps] + self.config.state_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None, self.config.timesteps] + self.config.state_size, name="Y")

        # Make the network infraestructure here
        # Dynamically generating the lstm layers, for experimenting purposes
        lstms = [tf.nn.rnn_cell.LSTMCell(size) for size in self.config.lstm_sizes]
        # Adding dropout to each cell
        drops = [tf.nn.rnn_cell.DropoutWrapper(lstm, output_keep_prob=self.config.keep_prob) for lstm in lstms]

        # Stacking up the layers for deep learning
        cell = tf.nn.rnn_cell.MultiRNNCell(drops)

        # Setting up initial state to all zeros
        initial_state = cell.zero_state(self.config.batch_size, tf.float32)
        self.lstm_outputs, self.state = tf.nn.dynamic_rnn(cell, self.x, initial_state=initial_state)

        # Pass the output through a fully connected layer and get the predictions
        self.prediction = tf.contrib.layers.fully_connected(self.lstm_outputs, self.config.state_size[0], activation_fn=tf.nn.sigmoid)





        with tf.name_scope("loss"):
            loss = tf.losses.mean_squared_error(labels=self.y, predictions=self.prediction)
            self.cross_entropy = tf.reduce_mean(loss)
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy, global_step=self.global_step_tensor)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
