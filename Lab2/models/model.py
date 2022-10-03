import os
import numpy as np

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import tensorflow as tf


class FashionMNIST():
    def __init__(self, input_shape):
        self.model = tf.keras.models.Sequential()
        
        self.input_shape = input_shape
        self.batch_norm = tf.keras.layers.BatchNormalization
        self.conv2d = tf.keras.layers.Conv2D
        self.max_pooling = tf.keras.layers.MaxPooling2D
        self.dropout = tf.keras.layers.Dropout
        self.flatten = tf.keras.layers.Flatten
        self.dense = tf.keras.layers.Dense
        self.activation = tf.keras.layers.Activation
        
        self.labels = ['t_shirt', 'trouser', 'pullover', 'dress', 'coat', 'sandal', 'shirt', 'sneaker', 'bag', 'ankle_boots']
        
        self.create_model()
    

    def create_model(self):
        self.model.add(self.batch_norm(input_shape=self.input_shape))
        self.model.add(self.conv2d(64, (5, 5), padding='same', activation='elu'))
        self.model.add(self.max_pooling(pool_size=(2, 2), strides=(2,2)))
        self.model.add(self.dropout(0.25))

        self.model.add(self.batch_norm(input_shape=self.input_shape))
        self.model.add(self.conv2d(128, (5, 5), padding='same', activation='elu'))
        self.model.add(self.max_pooling(pool_size=(2, 2)))
        self.model.add(self.dropout(0.25))

        self.model.add(self.batch_norm(input_shape=self.input_shape))
        self.model.add(self.conv2d(256, (5, 5), padding='same', activation='elu'))
        self.model.add(self.max_pooling(pool_size=(2, 2), strides=(2,2)))
        self.model.add(self.dropout(0.25))

        self.model.add(self.flatten())
        self.model.add(self.dense(256))
        self.model.add(self.activation('elu'))
        self.model.add(self.dropout(0.5))
        self.model.add(self.dense(10))
        self.model.add(self.activation('softmax'))

    
    def load_weights(self, weights_path):
        self.model.load_weights(weights_path)

    
    def predict(self, X):
        try:
            X = X.reshape(-1, *X.shape)
            preds = self.model.predict(X)
            label = self.labels[np.argmax(preds)]
            confidence = np.max(preds)

            return label, str(round(confidence * 100, 2))
        except Exception:
            return None, None
        