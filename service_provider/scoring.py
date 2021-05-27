import numpy as np
import tensorflow as tf
from tensorflow import keras
import os
from pathlib import Path
from tensorflow.keras.preprocessing.image import load_img, img_to_array


model_dir = Path(os.path.dirname(__file__)).resolve().parent / 'models'


models = {
    'face': keras.models.load_model(model_dir / '21-05-14_13-02-04.h5'),
    'eye': keras.models.load_model(model_dir / '21-05-18_02-24-03-eye.h5'),
    'nose': keras.models.load_model(model_dir / '21-05-18_02-35-27-nose.h5'),
    'mouth': keras.models.load_model(model_dir / '21-05-18_03-10-50-mouth.h5'),
}

sizes = {
    "face": (300, 300),
    "eye": (50, 50),
    "nose": (60, 55),
    "mouth": (80, 50),
}


def scoring(images_numpy, detector='face'):
    resized_images = []

    for image in images_numpy:
        resized_images.append(tf.image.resize(image, sizes[detector]))

    result = models[detector].predict(np.array(resized_images))

    output = []

    for item_tuple in result:
        output.append([float(pos) for pos in item_tuple])

    return output


parts = ['face', 'eye', 'nose', 'mouth']


def read_pos_set(pos_set: str):
    parts_map = {}

    for part in parts:
        parts_map[part] = []

    for i, part_poses in enumerate(pos_set.split('&')):
        for pos in part_poses.split('|'):
            parts_map[parts[i]].append([int(item) for item in pos.split(',')])

    return parts_map


# def main():
#     print(scoring(
#         np.array([img_to_array(
#             load_img(
#                 '/home/chardon/Documents/source/project/face-aware/dataset/mouths_out/25.png'
#             )
#             )]), 'mouth'
#         )
#     )
#
#
# if __name__ == '__main__':
#     main()
