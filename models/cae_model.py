from base.base_model import BaseModel
import tensorflow as tf
import numpy as np

class CAEModel(BaseModel):
    def __init__(self,config):
        super(CAEModel,self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool, name="training")
        if (self.config.keep_prob < 1):
            print("REMEMBER THAT DROPOUT SHOULD ONLY BE USED FOR TRAINING")

        self.x = tf.placeholder(tf.float32, shape=[None] + self.config.state_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None] + self.config.state_size, name="Y")

        # Make the network infraestructure here
        # Encoder
        with tf.name_scope("encoder"):
            l1 = tf.layers.conv2d(inputs=self.x, filters=4, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv1")
            d1 = tf.nn.dropout(l1, self.config.keep_prob, name="e_drop1")
            # now 128x128x4
            l2 = tf.layers.max_pooling2d(d1, pool_size=(2,2), strides=(2,2), padding='same')
            # now 64x64x4
            l3 = tf.layers.conv2d(inputs=l2, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv2")
            d3 = tf.nn.dropout(l3, self.config.keep_prob, name="e_drop2")
            # now 64x64x8
            l4 = tf.layers.max_pooling2d(d3, pool_size=(2,2), strides=(2,2), padding='same')
            # now 32x32x8
            l5 = tf.layers.conv2d(inputs=l4, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv3")
            d5 = tf.nn.dropout(l5, self.config.keep_prob, name="e_drop3")
            # now 32x32x16
            l6 = tf.layers.max_pooling2d(d5, pool_size=(2,2), strides=(2,2), padding='same')
            # now 16x16x16
            l7 = tf.layers.conv2d(inputs=l6, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv4")
            d7 = tf.nn.dropout(l7, self.config.keep_prob, name="e_drop4")
            # now 16x16x32
            l8 = tf.layers.max_pooling2d(d7, pool_size=(2,2), strides=(2,2), padding='same')
            # now 8x8x32
            l9 = tf.layers.conv2d(inputs=l8, filters=64, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv5")
            d9= tf.nn.dropout(l9, self.config.keep_prob, name="e_drop5")
            # now 8x8x64
            l10 = tf.layers.max_pooling2d(d9, pool_size=(2,2), strides=(2,2), padding='same')
            # now 4x4x64
            l11 = tf.layers.conv2d(inputs=l10, filters=128, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv6")
            d11= tf.nn.dropout(l11, self.config.keep_prob, name="e_drop6")
            # now 4x4x128
            l12 = tf.layers.max_pooling2d(d11, pool_size=(2,2), strides=(2,2), padding='same')
            # now 2x2x128
            l13 = tf.layers.conv2d(inputs=l12, filters=256, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv7")
            d13= tf.nn.dropout(l13, self.config.keep_prob, name="e_drop7")
            # now 2x2x512
            l14 = tf.layers.max_pooling2d(d13, pool_size=(2,2), strides=(2,2), padding='same')
            # now 1x1x512
            l15 = tf.layers.conv2d(inputs=l14, filters=512, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv8")
            d15= tf.nn.dropout(l15, self.config.keep_prob, name="encoded_drop")
            # now 2x2x512
        self.encoded = tf.layers.conv2d(inputs=l14, filters = 128, kernel_size=(5,5), padding='same', name='encoded')
        d16= tf.nn.dropout(self.encoded, self.config.keep_prob, name="encoded_drop")
        # now 1x1x1024
        with tf.name_scope("decoder"):
            dl14 = tf.layers.conv2d(inputs=d16, filters=512, kernel_size=(5,5), padding='same', name='d_conv0')
            d15= tf.nn.dropout(dl14, self.config.keep_prob, name="d_drop7")
            # now 1x1x512
            dl15 = tf.layers.conv2d(inputs=d15, filters=256, kernel_size=(5,5), padding='same', name='d_conv1')
            dd15= tf.nn.dropout(dl15, self.config.keep_prob, name="e_drop8")
            # now 1x1x512
            l16 = tf.image.resize_images(dd15, size=(2,2), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 2x2x512
            l17 = tf.layers.conv2d(inputs=l16, filters=128, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv2")
            d17 = tf.nn.dropout(l17, self.config.keep_prob, name="d_drop2")
            # now 2x2x128
            l18 = tf.image.resize_images(d17, size=(4,4), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 4x4x128
            l19 = tf.layers.conv2d(inputs=l18, filters=64, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv3")
            d19 = tf.nn.dropout(l19, self.config.keep_prob, name="d_drop3")
            # now 4x4x64
            l20 = tf.image.resize_images(d19, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 8x8x64
            l21 = tf.layers.conv2d(inputs=l20, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv4")
            d21 = tf.nn.dropout(l21, self.config.keep_prob, name="d_drop4")
            # now 8x8x32
            l22 = tf.image.resize_images(d21, size=(16,16), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 16x16x32
            l23 = tf.layers.conv2d(inputs=l22, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv5")
            d23 = tf.nn.dropout(l23, self.config.keep_prob, name="d_drop5")
            # now 16x16x16
            l24 = tf.image.resize_images(d23, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 32x32x16
            l25 = tf.layers.conv2d(inputs=l24, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv6")
            d25 = tf.nn.dropout(l25, self.config.keep_prob, name="d_drop6")
            # now 32x32x8
            l26 = tf.image.resize_images(d25, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 64x64x8
            l27 = tf.layers.conv2d(inputs=l26, filters=4, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv7")
            d27 = tf.nn.dropout(l27, self.config.keep_prob, name="d_drop7")
            # now 64x64x4
            l28 = tf.image.resize_images(d27, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 128x128x4
        self.decoded = tf.layers.conv2d(inputs=l28, filters=1, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="decoded")
        # now 128x128x1

        with tf.name_scope("loss"):
            # loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=self.y, logits=logits)
            loss = tf.losses.mean_squared_error(labels=self.y, predictions=self.decoded)
            # loss = tf.reduce_mean(tf.square(self.y - self.decoded))
            # loss = np.sum((self.y - self.decoded)**2)
            reg_losses = tf.get_collection(tf.GraphKeys.REGULARIZATION_LOSSES)
            self.cross_entropy = tf.reduce_sum(loss) + self.config.reg_constant*sum(reg_losses)
            # self.cross_entropy = loss#  + self.config.reg_constant*sum(reg_losses)
            update_ops = tf.get_collection(tf.GraphKeys.UPDATE_OPS)
            with tf.control_dependencies(update_ops):
                self.train_step = tf.train.AdamOptimizer(self.config.learning_rate).minimize(self.cross_entropy, global_step=self.global_step_tensor)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
