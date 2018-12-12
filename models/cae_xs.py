from base.base_model import BaseModel
import tensorflow as tf

class CAEModel(BaseModel):
    def __init__(self,config):
        super(CAEModel,self).__init__(config)
        self.build_model()
        self.init_saver()

    def build_model(self):
        self.is_training = tf.placeholder(tf.bool, name="training")

        self.x = tf.placeholder(tf.float32, shape=[None] + self.config.state_size, name="X")
        self.y = tf.placeholder(tf.float32, shape=[None] + self.config.state_size, name="Y")

        # Make the network infraestructure here
        # Encoder
        l1 = tf.layers.conv2d(inputs=self.x, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv1")
        # now 128x128x8
        l2 = tf.layers.max_pooling2d(l1, pool_size=(2,2), strides=(2,2), padding='same')
        # now 64x64x8
        l3 = tf.layers.conv2d(inputs=l2, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv2")
        # now 64x64x8
        l4 = tf.layers.max_pooling2d(l3, pool_size=(2,2), strides=(2,2), padding='same')
        # now 32x32x8
        l5 = tf.layers.conv2d(inputs=l4, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv3")
        # now 32x32x16
        l6 = tf.layers.max_pooling2d(l5, pool_size=(4,4), strides=(4,4), padding='same')
        # now 8x8x16
        l7 = tf.layers.conv2d(inputs=l6, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv4")
        # now 8x8x32
        l8 = tf.layers.max_pooling2d(l7, pool_size=(4,4), strides=(4,4), padding='same')
        # now 2x2x32
        self.encoded = tf.layers.conv2d(inputs=l8, filters=4, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="e_conv5")
        # now 2x2x4
        l10 = tf.layers.conv2d(inputs=self.encoded, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv1")
        # now 2x2x32
        l11 = tf.image.resize_images(l10, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 8x8x32
        l12 = tf.layers.conv2d(inputs=l11, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv2")
        # now 8x8x16
        l13 = tf.image.resize_images(l12, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 32x32x16
        l14 = tf.layers.conv2d(inputs=l13, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv3")
        # now 32x32x8
        l15 = tf.image.resize_images(l14, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 64x64x8
        l16 = tf.layers.conv2d(inputs=l15, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv4")
        # now 64x64x4
        l17 = tf.image.resize_images(l16, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        # now 128x128x4
        logits = tf.layers.conv2d(inputs=l17, filters=1, kernel_size=(5,5), padding='same', activation=None, kernel_initializer=tf.contrib.layers.xavier_initializer(), name="d_conv5")
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
