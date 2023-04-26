import numpy as np
import cv2
from keras.models import load_model
from pathlib import Path
filePath = Path(__file__).resolve().parent


def showImg(img):
    cv2.imshow("img", img)
    cv2.waitKey()


def emotion_analyze(img_url):
    # 加載已經訓練好的模型
    model = load_model(filePath/'0426.h5')

    # 讀取新的狗圖像
    img = cv2.imread(img_url)
    # showImg(img)

    img = cv2.resize(img, (224, 224))
    # showImg(img)

    # 預處理圖像
    img = img.astype('float32') / 255.0
    # showImg(img)

    img = np.expand_dims(img, axis=0)
    # print(model.summary())
    # img = np.reshape(img, (-1, 4 * 4 * 512))
    # showImg(img)
    # 進行預測
    predictions = model.predict(img)
    emo = ["angry", "happy", "relax", "sad"]
    print(predictions)
    return emo[np.argmax(predictions)]


# emotion_analyze(str(filePath/'img/0RXraPIKC00Dz1qkuMbj8XbuR80g5Z893.jpeg'))
