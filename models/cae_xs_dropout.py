from base.base_model import BaseModel
import tensorflow as tf

class CAEModel(BaseModel):
    def __init__(self,config):
        super(CAEModel,self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool, name="training")
        if (self.config.keep_prob > 0):
            print("REMEMBER THAT DROPOUT SHOULD ONLY BE USED FOR TRAINING")

        self.x = tf.placeholder(tf.float32, shape=[None] + self.config.state_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None] + self.config.state_size, name="Y")

        # Make the network infraestructure here
        # Encoder
        l1 = tf.layers.conv2d(inputs=self.x, filters=4, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv1")
        d1 = tf.nn.dropout(l1, self.config.keep_prob, name="drop1")
        # now 128x128x4
        l2 = tf.layers.max_pooling2d(d1, pool_size=(2,2), strides=(2,2), padding='same')
        # now 64x64x4
        l3 = tf.layers.conv2d(inputs=l2, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv2")
        d3 = tf.nn.dropout(l3, self.config.keep_prob, name="drop2")
        # now 64x64x8
        l4 = tf.layers.max_pooling2d(d3, pool_size=(2,2), strides=(2,2), padding='same')
        # now 32x32x8
        l5 = tf.layers.conv2d(inputs=l4, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv3")
        d5 = tf.nn.dropout(l5, self.config.keep_prob, name="drop3")
        # now 32x32x16
        l6 = tf.layers.max_pooling2d(d5, pool_size=(2,2), strides=(2,2), padding='same')
        # now 16x16x16
        l7 = tf.layers.conv2d(inputs=l6, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv4")
        d7 = tf.nn.dropout(l7, self.config.keep_prob, name="drop4")
        # now 16x16x32
        l8 = tf.layers.max_pooling2d(d7, pool_size=(2,2), strides=(2,2), padding='same')
        # now 8x8x32
        l9 = tf.layers.conv2d(inputs=l8, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv5")
        d9= tf.nn.dropout(l9, self.config.keep_prob, name="drop5")
        # now 8x8x32
        l10 = tf.layers.max_pooling2d(d9, pool_size=(4,4), strides=(4,4), padding='same')
        # now 2x2x32
        self.encoded = tf.layers.conv2d(inputs=l10, filters = 4, kernel_size=(7,7), padding='same', name='encoded')
        # now 2x2x4
        l11 = tf.layers.conv2d(inputs=self.encoded, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv1")
        d11 = tf.nn.dropout(l11, self.config.keep_prob, name="drop11")
        # now 2x2x32
        l12 = tf.image.resize_images(d11, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 8x8x32
        l13 = tf.layers.conv2d(inputs=l12, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv2")
        d13 = tf.nn.dropout(l13, self.config.keep_prob, name="drop12")
        # now 8x8x32
        l14 = tf.image.resize_images(d13, size=(16,16), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 16x16x32
        l15 = tf.layers.conv2d(inputs=l14, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv3")
        d15 = tf.nn.dropout(l15, self.config.keep_prob, name="drop13")
        # now 16x16x16
        l16 = tf.image.resize_images(d15, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 32x32x16
        l17 = tf.layers.conv2d(inputs=l16, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv4")
        d17 = tf.nn.dropout(l17, self.config.keep_prob, name="drop14")
        # now 32x32x8
        l18 = tf.image.resize_images(d17, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 64x64x8
        l19 = tf.layers.conv2d(inputs=l18, filters=4, kernel_size=(7,7), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv5")
        d19 = tf.nn.dropout(l19, self.config.keep_prob, name="drop15")
        # now 64x64x4
        l19 = tf.image.resize_images(d19, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 128x128x4
        logits = tf.layers.conv2d(inputs=l19, filters=1, kernel_size=(7,7), padding='same', activation=None, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv6")
        # now 128x128x1
        self.decoded = tf.nn.sigmoid(logits, name="decoded")

        with tf.name_scope("loss"):
            loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=self.y, logits=logits)
            reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
            self.cross_entropy = tf.reduce_mean(loss) + self.config.reg_constant*sum(reg_losses)
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy, global_step=self.global_step_tensor)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
