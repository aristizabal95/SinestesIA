from base.base_model import BaseModel
import tensorflow as tf
import numpy as np

class ActionsModel(BaseModel):
    def __init__(self,config):
        super(ActionsModel,self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool, name="training")
        self.mean = tf.get_variable("mean", shape=(self.config.input_size), trainable=False)
        self.stdev = tf.get_variable("stdev", shape=(self.config.input_size), trainable=False)

        self.x = tf.placeholder(tf.float32, shape=[None] + self.config.input_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None] + self.config.output_size, name="Y")

        # Make the network infraestructure here
        # First normalize the input
        # Pass the output through a fully connected layer and get the predictions
        # Set the input as the first layer. This 'layer' variable will be replaced by the layer loop later
        layer = (self.x-self.mean)/self.stdev
        for hidden_size in self.config.layers:
            layer = tf.contrib.layers.fully_connected(layer, hidden_size, activation_fn=tf.nn.relu)
            layer = tf.nn.dropout(layer, keep_prob=self.config.keep_prob)
        logits = tf.contrib.layers.fully_connected(layer, self.config.output_size[0], activation_fn=None)
        # compress the results into values between -1 and 1
        self.prediction = logits





        with tf.name_scope("loss"):
            loss = tf.losses.mean_squared_error(labels=self.y, predictions=self.prediction)
            reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
            self.cross_entropy = tf.reduce_mean(loss) + self.config.reg_constant*sum(reg_losses)
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy, global_step=self.global_step_tensor)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
