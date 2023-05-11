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
emotion_labels = ['angry', 'happy', 'relaxed', 'sad']


def predict_one_img(img_path):
    pic_path = img_path
    img = Image.open(pic_path)
    img = img.resize((150, 150))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)

    features = conv_base.predict(img_array)
    features = np.reshape(features, (1, 4 * 4 * 512))

    prediction = model.predict(features)
    predicted_label = emotion_labels[np.argmax(prediction)]
    print(f"Predicted emotion: {predicted_label}")
    return np.argmax(prediction)


all_count = []
for i, label in enumerate(emotion_labels):
    count = 0
    for img in os.listdir(file_path/'content/Dog Emotion/val'/label):
        emo_index = predict_one_img(
            str(file_path/'content/Dog Emotion/val'/label/img))
        if emo_index == i:
            count += 1
    print(f"{emotion_labels[i]},{count}")
    all_count.append(count)
print(all_count)
    