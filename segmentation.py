import keras
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageChops
import tensorflow as tf
import keras.backend as K
import os
from io import BytesIO
import requests
from keras.models import load_model
import numpy as np
from skimage.io import imread
from skimage.color import rgb2lab, lab2rgb, rgb2gray, gray2rgb
from skimage.transform import resize
from keras.models import model_from_json
from helpers import *


# for testing segmentation locally
# impath = '<PATH OF IMAGE TO TO TEST>'

_height = 256
_width = 256

count = np.random.randint(low=0, high=10000)


def create_path():
    return "static/assets/temp" + str(count) + ".png"


def dice_coef(y_true, y_pred, smooth=1):
    """
    Dice = (2*|X & Y|)/ (|X|+ |Y|)
         =  2*sum(|A*B|)/(sum(A^2)+sum(B^2))
    ref: https://arxiv.org/pdf/1606.04797v1.pdf
    """
    intersection = K.sum(K.abs(y_true * y_pred), axis=-1)
    return K.mean(
        (2.0 * intersection + smooth)
        / (K.sum(K.square(y_true), -1) + K.sum(K.square(y_pred), -1) + smooth)
    )


def dice_coef_loss(y_true, y_pred):
    return 1 - dice_coef(y_true, y_pred)


def OneImage(impath):
    return resize(imread(impath), (256, 256, 3))


def ELA(img):
    original = img
    TEMP = "static/assets/ela_temp.jpg"
    scale = 10
    quality = 90
    diff = ""
    try:
        original.save(TEMP, quality=90)
        temporary = Image.open(TEMP)
        diff = ImageChops.difference(original, temporary)

    except:

        original.convert("RGB").save(TEMP, quality=90)
        temporary = Image.open(TEMP)
        diff = ImageChops.difference(original.convert("RGB"), temporary)

    d = diff.load()
    WIDTH, HEIGHT = diff.size
    for x in range(WIDTH):
        for y in range(HEIGHT):
            d[x, y] = tuple(k * scale for k in d[x, y])

    return diff


def convert_to_3_channel(img):
    arr = np.array(img)
    arr = (arr >= 0.14) * 1.0
    arr = np.stack([arr, arr, arr], axis=2)
    #     print(arr.shape)
    arr = arr.reshape((1, 256, 256, 3))
    return arr


def segment_image(impath):
    img = ""
    try:
        response = requests.get(impath)
        img = Image.open(BytesIO(response.content)).convert("RGB")
    except:
        # if you want to locally import the image from path then comment above line
        # Uncomment the below line
        img = Image.open(impath).convert("RGB")
    # response = requests.get(impath)
    # s3 se fetch image ko
    # img = Image.open(BytesIO(response.content)).convert("RGB")

    # if you want to locally import the image from path then comment above line
    # Uncomment the below line
    # img = Image.open(impath).convert('RGB')

    img = img.resize((_height, _width), Image.ANTIALIAS)

    ela_image = ELA(img)
    ela_image.save("static/assets/ela_temp.png")
    # ela_image = imread('ela_temp.jpg')
    # img = LoadImages(ela_image)

    json_file = open("models/segmentation/model.json", "r")
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights("models/segmentation/model_for_json.h5")

    loaded_model.compile(loss=dice_coef_loss, optimizer="adam", metrics=[dice_coef])

    img = OneImage("static/assets/ela_temp.png")
    img = img.reshape((-1, 256, 256, 3))

    img = tf.convert_to_tensor(img, dtype="float32")
    predicted = loaded_model.predict(img)

    img2 = (predicted[0] >= 0.14) * 1.0
    mat = np.reshape(img2, (256, 256))
    img = Image.fromarray(np.uint8(mat * 255), "L")
    global count
    count = np.random.randint(low=0, high=10000)
    new_path = create_path()
    img.save(new_path)
    return new_path


# segment_image('<PATH TO THE IMAGE FILE>')
