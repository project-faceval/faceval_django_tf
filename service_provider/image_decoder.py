import uuid
from pathlib import Path
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img, img_to_array


tmp_root = Path('/tmp/faceval-python/django/ml/').resolve()


def get_uuid():
    return str(uuid.uuid1())


def decode_binary(binary_img, ext):
    file_path = tmp_root / f"{get_uuid()}.{ext}"

    if not tmp_root.exists():
        os.makedirs(tmp_root)

    with open(file_path, 'wb+') as f:
        for chunk in binary_img.chunks():
            f.write(chunk)

    # img = cv.imread(str(file_path))
    img = img_to_array(load_img(file_path))
    os.remove(file_path)
    return img
