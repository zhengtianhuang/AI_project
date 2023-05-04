# predict.py
'''
引用庫
'''
import numpy as np
import cv2
from keras.models import load_model
from pathlib import Path
import matplotlib.pyplot as plt
'''
變數區
'''
filePath = Path(__file__).resolve().parent.parent.parent
model = load_model(
    filePath/'checkpoints/0504/weights.01-2.14.h5')  # 加載已經訓練好的模型
'''
函式區
'''


def showImg(img):
    cv2.imshow("img", img)
    cv2.waitKey()


def predict_emotion(img_path):
    '''
    狗狗情緒分析
    :param  img_path : 圖片本地路徑
    :return 情緒
            - angry
            - happy
            - relax
            - sad
    '''
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
    return np.argmax(predictions)


    # return emo[np.argmax(predictions)]
plt.plot(model.history.history["categorical_accuracy"],
         c="r", label="train_accuracy")
plt.plot(
    model.history.history["val_categorical_accuracy"], c="b", label="test_accuracy")
plt.legend(loc="upper left")
plt.show()
