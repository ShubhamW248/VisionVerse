import tensorflow as tf
from PIL import Image
import numpy as np

def preprocess_image(image):
    img = tf.keras.preprocessing.image.img_to_array(image)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    return img

def deprocess_image(img):
    img = img[0]  # Remove batch dimension
    img = img * 0.5 + 0.5  # De-normalize from [-1, 1] to [0, 1]
    img = tf.image.convert_image_dtype(img, dtype=tf.uint8)  # Convert to uint8
    return img.numpy()

def generate_deepdream(image):
    model = tf.keras.applications.InceptionV3(include_top=False, weights='imagenet')
    
    # Choose a layer for dream visualization
    layer_name = 'mixed3'
    layer = model.get_layer(layer_name).output
    dream_model = tf.keras.Model(inputs=model.input, outputs=layer)
    
    # Implement DeepDream algorithm
    img = preprocess_image(image)
    
    @tf.function
    def deepdream_step(img, step_size):
        with tf.GradientTape() as tape:
            tape.watch(img)
            loss = tf.reduce_mean(dream_model(img))
        grads = tape.gradient(loss, img)
        grads /= tf.math.reduce_std(grads) + 1e-8 
        img += grads * step_size
        img = tf.clip_by_value(img, -1, 1)
        return loss, img
    
    # Run gradient ascent
    step_size = 0.01
    steps = 100
    for step in range(steps):
        loss, img = deepdream_step(img, step_size)
    
    return Image.fromarray(deprocess_image(img))
