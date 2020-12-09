import numpy as np
from matplotlib import image
import matplotlib.pyplot as plt
import keras
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.optimizers import SGD
from keras.layers import Dense, Flatten, Input, Dropout
from keras.applications import VGG16

class Predictions:
    
    vgg = VGG16(
        include_top = False,
        input_shape = (224, 224, 3)
    )
    
    def __init__(self, model = False):
        if not model:
            self.loaded_model = False
        else:
            self.loaded_model = True
        self.model = model
        self.loaded_image = False
        self.loaded_image_features = False
        
    def load_image(self, filename, save_image=True):
        # load the image
        img = load_img(filename, target_size=(224, 224))
        # convert to array
        img = img_to_array(img)
        # reshape into a single sample with 3 channels
        img = img.reshape(1, 224, 224, 3)
        # center pixel data
        img = img.astype('float32')
        img = img - [123.68, 116.779, 103.939]
        if save_image:
            self.filename = filename
            self.image = img
            self.loaded_image = True
        return img
    
    def get_bottleneck_features(self, save_features=True):
        if not self.loaded_image:
            raise ValueError('Must load an image before generating features. Call the load_image method and set save_image to True')
        model = VGG16(
            include_top = False,
            input_shape = (224, 224, 3)
        )
        image_features = model.predict(self.image)
        if save_features:
            self.image_features = image_features
            self.loaded_image_features = True
        return image_features
    
    def load_model(self, weights_filepath = '/Users/vinnythompson/Documents/Metis/project5/website/personal_website/model_weights/weights-57-0.928.hdf5'):
        inputs = Input(shape = (7,7,512))
        flat = Flatten(input_shape=inputs.shape[1:])(inputs)
        class1 = Dense(256, activation='relu')(flat)
        drop1 = Dropout(0.3)(class1)
        class2 = Dense(128, activation='relu')(drop1)
        drop2 = Dropout(0.65)(class2)
        class3 = Dense(64, activation='relu')(drop2)
        drop3 = Dropout(0.15)(class3)
        output = Dense(1, activation='sigmoid')(drop3)

        model = keras.Model(inputs=inputs, outputs = output)

        opt = SGD(lr=0.001, momentum=0.9)
        model.compile(optimizer=opt,
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        model.load_weights(weights_filepath)
        self.model = model
        self.loaded_model = True
    
    def predict(self, filename):
        img = self.load_image(filename)
        image_features = self.get_bottleneck_features()
        if not self.loaded_model:
            self.load_model()
        
        
        self.prediction = self.model(self.image_features, training=False).numpy()[0][0]
        if self.prediction >.5:
            print('Healthy')
        else:
            print('Conjunctivitis - consider seeing a medical professional')
#         data = image.imread(self.filename)
#         plt.imshow(data)
#         plt.show()
        return self.prediction
    
    def show_image(self):
        if not self.loaded_image:
            raise ValueError('Must load an image before printing. Call the load_image method and set save_image to True')
        data = image.imread(self.filename)
        plt.imshow(data)
        plt.show()