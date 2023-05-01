import numpy as np
import cv2
from keras.models import load_model
from pathlib import Path
filePath = Path(__file__).resolve().parent
model = load_model(filePath/'0426.h5')


def showImg(img):
    cv2.imshow("img", img)
    cv2.waitKey()


def emotion_analyze(img_path):
    # 加載已經訓練好的模型
    # 讀取新的狗圖像
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    # 預處理圖像
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    # 進行預測
    predictions = model.predict(img)
    emo = ["angry", "happy", "relax", "sad"]
    print(predictions)
    return emo[np.argmax(predictions)]
