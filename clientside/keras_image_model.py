import numpy as np
import tensorflow as tf
import h5py

input_img = keras.layers.Input(shape=(240,320,4))

x = keras.layers.Conv2D(12, (5,5), activation='relu', padding='same')(input_img)
x = keras.layers.MaxPooling2D((2,2), padding='same')(x)
x = keras.layers.Conv2D(6, (5,5), activation='relu', padding='same')(x)
x = keras.layers.MaxPooling2D((2,2), padding='same')(x)
x = keras.layers.Conv2D(4, (5,5), activation='relu', padding='same')(x)
x = keras.layers.MaxPooling2D((2,2), padding='same')(x)
x = keras.layers.Conv2D(3, (5,5), activation='relu', padding='same')(x)
encoded = keras.layers.MaxPooling2D((2,2), padding='same')(x)

# At this point the representation is (3, 5, 3) i.e. 45-dimensional

x = keras.layers.Conv2D(3, (5,5), activation='relu',padding='same')(encoded)
x = keras.layers.UpSampling2D((2,2))(x)
x = keras.layers.Conv2D(4, (5,5), activation='relu',padding='same')(x)
x = keras.layers.UpSampling2D((2,2))(x)
x = keras.layers.Conv2D(6, (5,5), activation='relu',padding='same')(x)
x = keras.layers.UpSampling2D((2,2))(x)
x = keras.layers.Conv2D(12, (5,5), activation='relu',padding='same')(x)
x = keras.layers.UpSampling2D((2,2))(x)
decoded = keras.layers.Conv2D(4, (5,5), activation='sigmoid',padding='same')(x)

autoencoder = keras.models.Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

# Retrieve the image dataset
f = h5py.File('raw_dataset.hdf5','r')
video = f['video']['2018_09_19_09_22_23']
video = np.rollaxis(video[:],1,4)
x_train = video / 255

autoencoder.fit(x_train,x_train,
                epochs=50,
                batch_size=128,
                shuffle=True,
                validation_data=(x_train,x_train),
                callbacks=[keras.callbacks.TensorBoard(log_dir='/tmp/autoencoder')])
