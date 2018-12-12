import numpy as np
import tensorflow as tf
import h5py
import os
import matplotlib.pyplot as plt

# load the dataset
f = h5py.File('raw_dataset.hdf5','r')
# for a start, we will only select the last recording inside the raw raw_dataset
# Later, the data will be split into train, validation and test datasets for
# proper model development
frames = f['video'][list(f['video'].keys())[3]][:]
frames = np.rollaxis(frames,1,4)
# frames contains images of dimensions 128x128x4
# normalize the data
frames = frames/frames.max()

# randomize the order and split into train, val and test
np.random.shuffle(frames)
train_percent = 0.7
cross_val_percent = 0.15
test_percent = 0.15
data_amount = frames.shape[0]

train_dset = frames[0:int(data_amount*train_percent)]
cross_dset = frames[int(data_amount*train_percent+1):int(data_amount*cross_val_percent)]
test_dset = frames[int(data_amount*0.85+1):]


#=============== LEARNING MODEL =================
# learning inputs
with tf.name_scope('input'):
    x = tf.placeholder(tf.float32, (None,128,128,4), name="X")
    y = tf.placeholder(tf.float32, (None,174), name="Y")
    tf.summary.histogram('x_input', x)

# Encoder
conv1 = tf.layers.conv2d(inputs=x, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 128x128x8
maxpool1 = tf.layers.max_pooling2d(conv1, pool_size=(2,2), strides=(2,2), padding='same')
# now 64x64x8
conv2 = tf.layers.conv2d(inputs=maxpool1, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 64x64x16
maxpool2 = tf.layers.max_pooling2d(conv2, pool_size=(2,2), strides=(2,2), padding='same')
# now 32x32x16
conv3 = tf.layers.conv2d(inputs=maxpool2, filters=32, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 32x32x32
maxpool3 = tf.layers.max_pooling2d(conv3, pool_size=(2,2), strides=(2,2), padding='same')
# now 16x16x32
conv4 = tf.layers.conv2d(inputs=maxpool3, filters=64, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 16x16x64
maxpool4 = tf.layers.max_pooling2d(conv4, pool_size=(2,2), strides=(2,2), padding='same')
# now 8x8x64
conv5 = tf.layers.conv2d(inputs=maxpool4, filters=128, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 8x8x128
# encoded = tf.layers.max_pooling2d(conv5, pool_size=(2,2), strides=(2,2), padding='same')
encoded = conv5
# now 4x4x128

tf.summary.histogram('encoding',encoded)

#Decoder
# upsample1 = tf.image.resize_images(encoded, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
upsample1 = encoded
# now 8x8x128
conv5 = tf.layers.conv2d(inputs=upsample1, filters=32, kernel_size=(7,7), padding='same',activation=tf.nn.relu)
# now 8x8x64
upsample2 = tf.image.resize_images(conv5, size=(16,16), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 16x16x64
conv6 = tf.layers.conv2d(inputs=upsample2, filters=32, kernel_size=(7,7), padding='same',activation=tf.nn.relu)
# now 16x16x32
upsample3 = tf.image.resize_images(conv6, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 32x32x32
conv7 = tf.layers.conv2d(inputs=upsample3, filters=16, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 32x32x16
upsample4 = tf.image.resize_images(conv7, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 64x64x16
conv8 = tf.layers.conv2d(inputs=upsample4, filters=8, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 64x64x8
upsample5 = tf.image.resize_images(conv8, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 64x64x16
logits = tf.layers.conv2d(inputs=upsample5, filters=4, kernel_size=(7,7), padding='same', activation=tf.nn.relu)
# now 128x128x4

# pass logits through sigmoid to get reconstructed images
decoded = tf.nn.sigmoid(logits)
tf.summary.histogram("decoded", decoded)

#pass logits through sigmoid and calculate the cross-entropy loss
# loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=y,logits=logits)
loss = tf.losses.mean_squared_error(labels=y,predictions=logits)

# learning params
learning_rate = 0.0001
batch_size = 10
epochs = 40
# Get the cost and define the optimizer
cost = tf.reduce_mean(loss)
tf.summary.scalar('cost',cost)
opt = tf.train.AdamOptimizer(learning_rate).minimize(cost)

# create the session
sess = tf.Session()

# Store the graph for tensorboard visualization
logs_dir = os.path.abspath(os.path.expanduser('logs/'))
summary_op = tf.summary.merge_all()
summary_writer = tf.summary.FileWriter(logs_dir, graph=sess.graph)
saver = tf.train.Saver()

last_ckpt = tf.train.latest_checkpoint('checkpoints/')
if last_ckpt is None:
    sess.run(tf.global_variables_initializer())
else:
    saver.restore(sess, last_ckpt)
    print("model restored")

# training
img = None
label = None
for e in range(epochs):
    for batch_i in range(train_dset.shape[0]//batch_size):
        batch = train_dset[batch_i*batch_size:batch_i*batch_size+batch_size]
        test_index = np.random.randint(test_dset.shape[0], size=1)[0]
        result = sess.run(decoded, feed_dict={x: test_dset[[test_index]]})
        plt.subplot(2,1,1)
        if img is None:
            img = plt.imshow(result[0])
        else:
            img.set_data(result[0])
        plt.subplot(2,1,2)
        if label is None:
            label = plt.imshow(test_dset[test_index])
        else:
            label.set_data(test_dset[test_index])
        plt.pause(0.0001)
        plt.draw()
        tf.summary.image('result_img', result)
        batch_cost, summary, _ = sess.run([cost,summary_op,opt], feed_dict={x: batch, y: batch})
        summary_writer.add_summary(summary)
        print('Epoch: '+ str(e) + '/' + str(epochs) + ', batch: '+ str(batch_i) + ', batch_cost: ' + str(batch_cost))
    save_path = saver.save(sess, "checkpoints/cae.ckpt")
