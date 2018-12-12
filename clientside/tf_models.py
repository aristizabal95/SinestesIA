import tensorflow as tf
import numpy as np
import os

class CAE:
    #Convolution Auto-Encoder Model factory
    # TODO Define model method which includes all tf operations (training as well) and return encoder, decoder and training ops
    def __init__(self, learning_rate=0.01, checkpoint_dir="checkpoints/cae.ckpt", log_dir="logs/"):
        self.graph = tf.get_default_graph()
        self.learning_rate = learning_rate
        self.input, self.label, self.encoder, self.decoder, self.cost, self.opt = self._model()
        self.sess = tf.Session()
        self.saver = tf.train.Saver()
        self.sess.run(tf.global_variables_initializer())
        # self.checkpoint_dir = checkpoint_dir
        # restored = self._restore(self.checkpoint_dir)
        # if restored:
        #     print("model restored")
        # else:
        #     init = tf.global_variables_initializer()
        #     self.sess.run(init)

    def _placeholders(self):
        x = tf.placeholder(tf.float32,(None,128,128,1),name="X")
        y = tf.placeholder(tf.float32,(None,128,128,1),name="Y")
        return x,y

    def _encoder(self, input):
        with tf.name_scope('encoder'):
            x = input
            # Encoder
            l1 = tf.layers.conv2d(inputs=x, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="e_conv1")
            # now 128x128x8
            l2 = tf.layers.max_pooling2d(l1, pool_size=(2,2), strides=(2,2), padding='same')
            # now 64x64x8
            l3 = tf.layers.conv2d(inputs=l2, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="e_conv2")
            # now 64x64x8
            l4 = tf.layers.max_pooling2d(l3, pool_size=(2,2), strides=(2,2), padding='same')
            # now 32x32x8
            l5 = tf.layers.conv2d(inputs=l4, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="e_conv3")
            # now 32x32x16
            l6 = tf.layers.max_pooling2d(l5, pool_size=(2,2), strides=(2,2), padding='same')
            # now 16x16x16
            l7 = tf.layers.conv2d(inputs=l6, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="e_conv4")
            # now 16x16x16
            l8 = tf.layers.max_pooling2d(l7, pool_size=(2,2), strides=(2,2), padding='same')
            # now 8x8x16
            l9 = tf.layers.conv2d(inputs=l8, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="e_conv5")
            # now 8x8x32
            l10 = tf.layers.max_pooling2d(l9, pool_size=(4,4), strides=(4,4), padding='same')
            # now 2x2x32
            l11 = tf.layers.conv2d(inputs=l10, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="encoded")
            # now 2x2x8
            return l11

    def _decoder(self, input):
        with tf.name_scope('decoder'):
            x_dec = input
            # Encoder
            l12 = tf.layers.conv2d(inputs=x_dec, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="d_conv1")
            # now 2x2x32
            l13 = tf.image.resize_images(l12, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 8x8x32
            l14 = tf.layers.conv2d(inputs=l13, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="d_conv2")
            # now 8x8x16
            l15 = tf.image.resize_images(l14, size=(16,16), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 16x16x16
            l16 = tf.layers.conv2d(inputs=l15, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="d_conv3")
            # now 16x16x16
            l17 = tf.image.resize_images(l16, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 32x32x16
            l18 = tf.layers.conv2d(inputs=l17, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="d_conv4")
            # now 32z32z8
            l19 = tf.image.resize_images(l18, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 64x64x8
            l20 = tf.layers.conv2d(inputs=l19, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="d_conv5")
            # now 64x64x8
            l21 = tf.image.resize_images(l20, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 128x128x8
            logits = tf.layers.conv2d(inputs=l21, filters=1, kernel_size=(5,5), padding='same', activation=tf.nn.relu, name="decoded_logits")
            # now 128x128x1
            decoded = tf.nn.sigmoid(logits, name="decoded")
            return decoded, logits #decoded for true result, logits for training purposes

    def _cost_fn(self, prediction, label):
        # loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=label, logits=logits)
        loss = tf.losses.mean_squared_error(labels=label,predictions=prediction)
        cost = tf.reduce_mean(loss)
        return cost

    def _optimizer(self, cost):
        global_step = tf.Variable(0, trainable=False, name='global_step')
        opt = tf.train.AdamOptimizer(self.learning_rate).minimize(cost, global_step=global_step)
        return opt


    def _model(self):
        x,y = self._placeholders()
        encoded = self._encoder(x)
        tf.summary.histogram("encoded", encoded)
        decoded, logits = self._decoder(encoded)
        tf.summary.histogram("decoded", decoded)
        cost = self._cost_fn(decoded, y)
        tf.summary.scalar('cost',cost)
        opt = self._optimizer(cost)
        return x, y, encoded, decoded, cost, opt


    def _restore(self, checkpoint_dir):
        last_ckpt = tf.train.latest_checkpoint(checkpoint_dir)
        if last_ckpt is None:
            return False
        else:
            self.saver.restore(self.sess, last_ckpt)
            print("model restored")
            return True

    def _train(self, data, labels, logs_dir="logs/", batch_size=20, epochs=10, noise_percent=15):
        logs_dir = os.path.abspath(os.path.expanduser(logs_dir))
        summary_op = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter(logs_dir, graph=self.sess.graph)
        for e in range(epochs): # TODO extract the minimizing step from the training process
            for batch_i in range(data.shape[0]//batch_size):
                batch = data[batch_i*batch_size:batch_i*batch_size+batch_size]
                labels = np.clip((batch-(noise_percent/100)), 0, 1) # Reduce noise
                labels = labels/labels.max() #normalize
                batch_cost, summary, _ = self.sess.run([self.cost,summary_op,self.opt], feed_dict={'X:0': batch, "Y:0": labels})
                print('Epoch: '+ str(e) + '/' + str(epochs) + ', batch: '+ str(batch_i) + ', batch_cost: ' + str(batch_cost))
                summary_writer.add_summary(summary)
                # if batch_i % 10 == 0:
                #     summary_writer.add_summary(summary)
                #     save_path = self.saver.save(self.sess, self.checkpoint_dir)
                #     print("Checkpoint saved")

#
    # def predict(input):
