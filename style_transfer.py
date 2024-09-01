import tensorflow as tf
import numpy as np
from PIL import Image
import os

# Path to the locally saved model
MODEL_PATH = r'C:\Users\asus\.cache\kagglehub\models\google\arbitrary-image-stylization-v1\tensorFlow1\256\2'

def load_img(path_to_img):
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = tf.image.resize(img, (256, 256))  # Resize to model input size
    img = img[tf.newaxis, :]
    return img

def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        tensor = tensor[0]
    return Image.fromarray(tensor)

def apply_style_transfer(content_path, style_path):
    content_image = load_img(content_path)
    style_image = load_img(style_path)

    # Load the locally saved Fast Neural Style Transfer model
    print("Loading model from local path...")
    model = tf.saved_model.load(MODEL_PATH)

    # Stylize the image
    stylized_image = model(tf.constant(content_image), tf.constant(style_image))[0]

    return tensor_to_image(stylized_image)