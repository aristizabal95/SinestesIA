import numpy as np
import tensorflow as tf
import h5py
import os
import matplotlib.pyplot as plt

# load the dataset
f = h5py.File('video_dataset.hdf5','r')
# for a start, we will only select the last recording inside the raw raw_dataset
# Later, the data will be split into train, validation and test datasets for
# proper model development
frames = f['video'][:,3,:,:]
# frames = f['video'][:]
# frames = np.rollaxis(frames,1,4)
# frames contains images of dimensions 128x128x4
# normalize the data
mask = np.abs(np.floor(frames/127)-1)
frames = frames*mask/frames.max()
frames = np.expand_dims(frames,axis=4)
replay = np.copy(frames)

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
    x = tf.placeholder(tf.float32, (None,128,128,1), name="X")
    y = tf.placeholder(tf.float32, (None,128,128,1), name="Y")
    tf.summary.histogram('x_input', x)

# Encoder
l1 = tf.layers.conv2d(inputs=x, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 128x128x32
l2 = tf.layers.max_pooling2d(l1, pool_size=(2,2), strides=(2,2), padding='same')
# now 64x64x32
l3 = tf.layers.conv2d(inputs=l2, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 64x64x16
l4 = tf.layers.max_pooling2d(l3, pool_size=(2,2), strides=(2,2), padding='same')
# now 32x32x16
l5 = tf.layers.conv2d(inputs=l4, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 32x32x16
l6 = tf.layers.max_pooling2d(l5, pool_size=(2,2), strides=(2,2), padding='same')
# now 16x16x16
l7 = tf.layers.conv2d(inputs=l6, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 16x16x16
l8 = tf.layers.max_pooling2d(l7, pool_size=(2,2), strides=(2,2), padding='same')
# now 8x8x16
l9 = tf.layers.conv2d(inputs=l8, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 8x8x8
l10 = tf.layers.max_pooling2d(l9, pool_size=(4,4), strides=(4,4), padding='same')
# now 2x2x8
l11 = tf.layers.conv2d(inputs=l10, filters=4, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 2x2x4

tf.summary.histogram('encoding',l11)

#Decoder
l12 = tf.layers.conv2d(inputs=l11, filters=8, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 2x2x8
l13 = tf.image.resize_images(l12, size=(8,8), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 8x8x8
l14 = tf.layers.conv2d(inputs=l13, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 8x8x16
l15 = tf.image.resize_images(l14, size=(16,16), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 16x16x4
l16 = tf.layers.conv2d(inputs=l15, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 16x16x16
l17 = tf.image.resize_images(l16, size=(32,32), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 32x32x16
l18 = tf.layers.conv2d(inputs=l17, filters=16, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 32x32x16
l19 = tf.image.resize_images(l18, size=(64,64), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 64x64x16
l20 = tf.layers.conv2d(inputs=l19, filters=32, kernel_size=(5,5), padding='same', activation=tf.nn.relu)
# now 64x64x32
l21 = tf.image.resize_images(l20, size=(128,128), method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
# now 128x128x32
logits = tf.layers.conv2d(inputs=l21, filters=1, kernel_size=(5,5), padding='same', activation=None)
# now 128x128x1

# pass logits through sigmoid to get reconstructed images
decoded = tf.nn.sigmoid(logits)
tf.summary.histogram("decoded", decoded)

#pass logits through sigmoid and calculate the cross-entropy loss
loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=y,logits=logits)
# loss = tf.losses.mean_squared_error(labels=y,predictions=decoded)

# learning params
learning_rate = 0.0001
tf.summary.scalar('learning_rate', learning_rate)
batch_size = 200
epochs = 25
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
count = 0
for e in range(epochs):
    for batch_i in range(train_dset.shape[0]//batch_size):
        print(count)
        batch = train_dset[batch_i*batch_size:batch_i*batch_size+batch_size]
        test_index = np.random.randint(test_dset.shape[0], size=1)[0]
        result = sess.run(decoded, feed_dict={x: test_dset[[test_index]]})
        count += 1
        count %= frames.shape[0]
        plt.subplot(2,1,1)
        if img is None:
            img = plt.imshow(np.squeeze(result[0]))
        else:
            img.set_data(np.squeeze(result[0]))
        plt.subplot(2,1,2)
        if label is None:
            label = plt.imshow(np.squeeze(test_dset[test_index]))
        else:
            label.set_data(np.squeeze(test_dset[test_index]))
        plt.pause(0.0001)
        plt.draw()
        tf.summary.image('result_img', result)
        batch_cost, summary, _ = sess.run([cost,summary_op,opt], feed_dict={x: batch, y: batch})
        summary_writer.add_summary(summary)
        print('Epoch: '+ str(e) + '/' + str(epochs) + ', batch: '+ str(batch_i) + ', batch_cost: ' + str(batch_cost))
    save_path = saver.save(sess, "checkpoints/cae.ckpt")
    learning_rate /= 3
