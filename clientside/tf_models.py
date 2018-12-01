import tensorflow as tf
import numpy as np
import os

class CAE:
    #Convolution Auto-Encoder Model factory
    # TODO Define model method which includes all tf operations (training as well) and return encoder, decoder and training ops
    def __init__(self, checkpoint_dir="checkpoints/", log_dir="logs/"):
        self.input = tf.placeholder(tf.float32, (None,128,128,1), name="input")
        self.label = tf.placeholder(tf.float32, (None,128,128,1), name="label")
        self.encoder, self.decoder, self.loss, self.cost, self.opt = self._model(self.input, self.label)
        self.sess = tf.InteractiveSession()
        self.saver = tf.train.Saver()
        restored = self._restore(checkpoint_dir)
        if restored:
            print("model restored")
        else:
            init = tf.global_variables_initializer()
            self.sess.run(init)

    def _encoder(self, input):
        with tf.name_scope('encoder'):
            x = input
            # Encoder
            l1 = tf.layers.conv2d(inputs=x, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 128x128x8
            l2 = tf.layers.max_pooling2d(l1, pool_size=(2,2), strides=(2,2), padding='same')
            # now 64x64x8
            l3 = tf.layers.conv2d(inputs=l2, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 64x64x8
            l4 = tf.layers.max_pooling2d(l3, pool_size=(2,2), strides=(2,2), padding='same')
            # now 32x32x8
            l5 = tf.layers.conv2d(inputs=l4, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 32x32x16
            l6 = tf.layers.max_pooling2d(l5, pool_size=(2,2), strides=(2,2), padding='same')
            # now 16x16x16
            l7 = tf.layers.conv2d(inputs=l6, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 16x16x16
            l8 = tf.layers.max_pooling2d(l7, pool_size=(2,2), strides=(2,2), padding='same')
            # now 8x8x16
            l9 = tf.layers.conv2d(inputs=l8, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 8x8x32
            l10 = tf.layers.max_pooling2d(l9, pool_size=(4,4), strides=(4,4), padding='same')
            # now 2x2x32
            l11 = tf.layers.conv2d(inputs=l10, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu, name="encoded")
            # now 2x2x8
            return l11

    def _decoder(self, input):
        with tf.name_scope('decoder'):
            x = input
            # Encoder
            l1 = tf.layers.conv2d(inputs=x, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 2x2x32
            l2 = tf.image.resize_images(l1, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 8x8x32
            l3 = tf.layers.conv2d(inputs=l2, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 8x8x16
            l4 = tf.image.resize_images(l3, size=(16,16), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 16x16x16
            l5 = tf.layers.conv2d(inputs=l4, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 16x16x16
            l6 = tf.image.resize_images(l5, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 32x32x16
            l7 = tf.layers.conv2d(inputs=l6, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 32z32z8
            l8 = tf.image.resize_images(l7, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 64x64x8
            l9 = tf.layers.conv2d(inputs=l8, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
            # now 64x64x8
            l10 = tf.image.resize_images(l9, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
            # now 128x128x8
            logits = tf.layers.conv2d(inputs=l10, filters=1, kernel_size=(7,7), padding='same', activation=tf.nn.relu, name="decoded_logits")
            # now 128x128x1
            decoded = tf.nn.sigmoid(logits, name="decoded")
            return decoded, logits #decoded for true result, logits for training purposes

    def _model(self, input, labels, learning_rate=0.001):
        encoded = self._encoder(input)
        tf.summary.histogram("encoded", encoded)
        decoded,logits = self._decoder(encoded)
        tf.summary.histogram("decoded", decoded)
        loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=labels, logits=logits)
        cost = tf.reduce_mean(loss)
        tf.summary.scalar('cost',cost)
        opt = tf.train.AdamOptimizer(learning_rate).minimize(cost)
        return encoded, decoded, loss, cost, opt


    def _restore(self, checkpoint_dir):
        last_ckpt = tf.train.latest_checkpoint(checkpoint_dir)
        if last_ckpt is None:
            return False
        else:
            self.saver.restore(self.sess, last_ckpt)
            print("model restored")
            return True

    def _train(self, data, labels, logs_dir="logs/", learning_rate=0.001, batch_size=20, epochs=10, noise_percent=15):
        logs_dir = os.path.abspath(os.path.expanduser(logs_dir))
        summary_op = tf.summary.merge_all()
        summary_writer = tf.summary.FileWriter(logs_dir, graph=self.sess.graph)
        for e in range(epochs): # TODO extract the minimizing step from the training process
            for batch_i in range(data.shape[0]//batch_size):
                batch = data[batch_i*batch_size:batch_i*batch_size+batch_size]
                labels = np.clip((batch-(noise_percent/100)), 0, 1) # Reduce noise
                labels = labels/labels.max() #normalize
                bach_cost, summary, _ = self.sess.run([cost,summary_op,opt], feed_dict={'input:0': batch, "label:0": labels})
                print('Epoch: '+ str(e) + '/' + str(epochs) + ', batch: '+ str(batch_i) + ', batch_cost: ' + str(batch_cost))

#
    # def predict(input):
