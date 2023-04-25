from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import tensorflow as tf
from pathlib import Path
import cv2
filePath = Path(__file__).resolve().parent

# 載入模型
model = tf.keras.models.load_model(filePath/'0425.h5', compile=False)

# 設定圖片尺寸及通道數
img_size = (48, 48)
img_channels = 1

# 讀取圖片
img_path = filePath/'img/2AoiPsaOr4YiEGxiOAhfMQpZ3K77nc168.jpeg'
img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, img_size)
img = np.reshape(img, (1, img_size[0], img_size[1], img_channels))
img = img.astype('float32') / 255.0

# 進行預測
emo = ['angry', 'happy', 'relaxed', 'sad']
predictions = model.predict(img)
label = np.argmax(predictions)
print(predictions)
print(emo[label])
