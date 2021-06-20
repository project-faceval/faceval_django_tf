import base64
import os
import uuid
from io import BytesIO
from pathlib import Path

from PIL import Image
from tensorflow.keras.preprocessing.image import load_img, img_to_array

tmp_root = Path('/tmp/faceval-python/django/ml/').resolve()


def get_uuid():
    return str(uuid.uuid1())


def decode_base64(base64_str: str):
    return BytesIO(base64.b64decode(base64_str))


def decode_binary(binary_img, ext, use_base64: bool):
    file_path = tmp_root / f"{get_uuid()}.{ext}"

    img = None

    if use_base64:
        img = Image.open(decode_base64(binary_img))

    if not tmp_root.exists():
        os.makedirs(tmp_root)

    with open(file_path, 'wb+') as f:
        if img is not None:
            img.save(f)
            img.close()
        else:
            for chunk in binary_img.chunks():
                f.write(chunk)

    # img = cv.imread(str(file_path))
    img = img_to_array(load_img(file_path))
    os.remove(file_path)
    return img
