from oxford     import Oxford
from random     import shuffle
from scipy.misc import imrotate
import numpy as np
import random
import cv2 


class Generator(object):

    def __init__(self):
        self.__train = Oxford().train()
        self.__valid = Oxford().valid()

    def __augment_rotation(self, image):
        angle = np.random.uniform(-30, 30)
        image = imrotate(image, angle) 
        return image

    def __augment_luminance(self, image):
        scale = np.random.uniform(0.25, 0.75)
        image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2HLS)
        image[:,:,1]  = image[:,:,1] * (0.25 + scale)
        image = cv2.cvtColor(image, cv2.COLOR_HLS2RGB)
        return image

    def __augment_translation(self, image):
        x = np.random.uniform(-40, 40)
        y = np.random.uniform(-40, 40)
        scale = np.float32([[1,0,x],[0,y,0]])
        image = cv2.warpAffine(image, scale, (224,224))
        return image

    def __augment_feature(self, image):
        image = self.__augment_rotation(image)
        image = self.__augment_translation(image)
        image = self.__augment_luminance(image)
        return image
 
    def __augment_label(self, image):
        image = self.__augment_rotation(image)
        image = self.__augment_translation(image)
        return image

    def train(self, batch_size):
        labels = features = []
        random.shuffle(self.__train)
        for i in range(batch_size):
            feature = self.__train[i][0]
            feature = self.__augment_feature(feature)
            features.append(feature)
            label = self.__train[i][0]
            label = self.__augment_label(label)
            labels.append(label)
        yield features, labels

    def valid(self, batch_size):
        labels = features = []
        random.shuffle(self.__valid)
        for i in range(batch_size):
            feature = self.__valid[i][0]
            feature = self.__augment_feature(feature)
            features.append(feature)
            label = self.__valid[i][0]
            label = self.__augment_label(label)
            labels.append(label)
        yield features, labels

