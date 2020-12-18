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
    
    def __init__(self, model = False):
        # attribute showing whether model weights have been provided or generated
        if not model:
            self.loaded_model = False 
        else:
            self.loaded_model = True
        #attribute containing model weights.  False if no weights have been provided or generated
        self.model = model
        #attribute showing whether the instance has been given an image to hold
        self.loaded_image = False
        #attribute containing image features.  False until get_bottleneck_features or predict method has been called
        self.loaded_image_features = False
        
    def load_image(self, filename, save_image=True):
        '''Return a 224 x 224 x 3 array containing image data of an input file

        filename (str): file location of input image
        save_image (bool): if True, array of image data will be saved in self.image and self.loaded_image will be set to True
        '''

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
        '''Return image features from output of final VGG16 convolutional layer. 

        save_features (bool): if True, image features will be saved in self.image_features and 
            self.loaded_image_featuers will be set to True
        '''

        # image must be loaded before calling get_bottleneck_features
        if not self.loaded_image:
            raise ValueError('Must load an image before generating features. Call the load_image method and set save_image to True')
        
        #instantiate VGG16 model
        model = VGG16(
            include_top = False,
            input_shape = (224, 224, 3)
        )

        #run image through VGG16 and store features
        image_features = model.predict(self.image)

        if save_features:
            self.image_features = image_features
            self.loaded_image_features = True

        return image_features
    
    def load_model(self, weights_filepath = '/Users/vinnythompson/Documents/Metis/project5/website/personal_website/model_weights/weights-57-0.928.hdf5'):
        '''Loads model weights if custom weights not provided
        '''

        # Create model architecture using Keras Functional API
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

        # Set optimizer to stochastic gradient descent
        opt = SGD(lr=0.001, momentum=0.9)
        model.compile(optimizer=opt,
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        # Load weights and save
        model.load_weights(weights_filepath)
        self.model = model
        self.loaded_model = True
    
    def predict(self, filename):
        '''Returns prediction for an image

        filename (str): file location of input image
        '''

        # Calls load_image method to generate 224 x 224 x 3 array
        img = self.load_image(filename)
        # Calls get_bottleneck_features method to run input image through VGG16
        image_features = self.get_bottleneck_features()
        # Calls load_model method if predict is being run for the first time
        if not self.loaded_model:
            self.load_model()
        
        # Gets prediction and stores it in self.prediction attribute
        self.prediction = self.model(self.image_features, training=False).numpy()[0][0]

        # Print prediction result
        if self.prediction >.5:
            print('Healthy')
        else:
            print('Conjunctivitis - consider seeing a medical professional')
        return self.prediction
    
    def show_image(self):
        '''Displays image contained in self.image
        '''

        if not self.loaded_image:
            raise ValueError('Must load an image before printing. Call the load_image method and set save_image to True')
        data = image.imread(self.filename)
        plt.imshow(data)
        plt.show()