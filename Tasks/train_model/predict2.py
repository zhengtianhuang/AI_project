from PIL import Image
import numpy as np
import os
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import load_model
from pathlib import Path
file_path = Path(__file__).resolve().parent
conv_base = VGG16(weights='imagenet',
                  include_top=False,             # 不包含 Full Connection
                  input_shape=(150, 150, 3))
model = load_model(file_path/'model/0504.h5')


def predict_one_img(img_path):
    pic_path = img_path
    img = Image.open(pic_path)
    img = img.resize((150, 150))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)

    features = conv_base.predict(img_array)
    features = np.reshape(features, (1, 4 * 4 * 512))

    prediction = model.predict(features)
    emotion_labels = ['angry', 'happy', 'relaxed', 'sad']
    predicted_label = emotion_labels[np.argmax(prediction)]
    print(f"Predicted emotion: {predicted_label}")


predict_one_img(
    file_path/'content/Dog Emotion/test/angry/0da4j6Ehkb6Ml0YBRiWmsBU2wEMoXP409.jpg')
