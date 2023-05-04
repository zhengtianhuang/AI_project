import tensorflow as tf
import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path
import json
print(tf.version)
filePath = Path(__file__).resolve().parent
img_dir = filePath/'content/Dog Emotion'
base_model = tf.keras.applications.InceptionV3(input_shape=(224, 224, 3),
                                               include_top=False,
                                               weights="imagenet")
# https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image/ImageDataGenerator

img_generator = tf.keras.preprocessing.image.ImageDataGenerator(
    # rotation_range=90,
    brightness_range=(0.5, 1),
    # shear_range=0.2,
    # zoom_range=0.2,
    channel_shift_range=0.2,
    horizontal_flip=False,
    vertical_flip=False,
    rescale=1./255,
    validation_split=0.3)

img_generator_flow_train = img_generator.flow_from_directory(
    directory=img_dir,
    target_size=(224, 224),
    batch_size=32,
    shuffle=True,
    subset="training")

img_generator_flow_valid = img_generator.flow_from_directory(
    directory=img_dir,
    target_size=(224, 224),
    batch_size=32,
    shuffle=True,
    subset="validation")
imgs, labels = next(iter(img_generator_flow_train))
base_model.trainable = False
model = tf.keras.Sequential([
    base_model,
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(4, activation="softmax")  # 4 classes
])
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
              loss=tf.keras.losses.CategoricalCrossentropy(),
              metrics=[tf.keras.metrics.CategoricalAccuracy()])

history = model.fit(img_generator_flow_train,
                    validation_data=img_generator_flow_valid,
                    steps_per_epoch=10, epochs=10)
model.save(filePath/'model/0504.h5')
with open(filePath/'model/0504.json', "w") as json_file:
    json.dump(history.to_json(), json_file)
