# predict.py
'''
引用庫
'''
import numpy as np
import cv2
from keras.models import load_model
from pathlib import Path
import os
'''
變數區
'''
file_path = Path(__file__).resolve().parent
model = load_model(
    file_path/'model/0426.h5')  # 加載已經訓練好的模型
emo = ["angry", "happy", "relaxed", "sad"]

'''
函式區
'''


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
    # print(emo[np.argmax(predictions)])
    return np.argmax(predictions)


all_count = []
for i, label in enumerate(emo):
    count = 0
    for img in os.listdir(file_path/'content/Dog Emotion/val'/label):
        emo_index = predict_emotion(
            str(file_path/'content/Dog Emotion/val'/label/img))
        if emo_index == i:
            count += 1
    print(f"{emo[i]},{count}")
    all_count.append(count)
print(all_count)
