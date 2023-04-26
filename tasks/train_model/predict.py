import numpy as np
import cv2
from keras.models import load_model
from pathlib import Path
filePath = Path(__file__).resolve().parent


def showImg(img):
    cv2.imshow("img", img)
    cv2.waitKey()


# 加載已經訓練好的模型
model = load_model(filePath/'0425.h5')

# 讀取新的狗圖像
img = cv2.imread(str(filePath/'img/0fmy0dTY2aV0kGQ8UEDgWDrbGyxnac904.jpeg'))
# showImg(img)

img = cv2.resize(img, (150, 150))
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
print(predictions)
