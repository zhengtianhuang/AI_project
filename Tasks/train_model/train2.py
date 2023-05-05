import numpy as np
import tensorflow as tf
from keras.applications import VGG16
from keras import models
from keras import layers
from keras import optimizers
import pandas as pd
import os
import random
import shutil
import json
from pathlib import Path
data_path = Path(__file__).resolve().parent/'content/Dog Emotion'

train_dir = os.path.join(data_path, "train")
val_dir = os.path.join(data_path, 'val')
test_dir = os.path.join(data_path, 'test')

batch_size = 25


def copy_data():
    # 讀取labels.csv檔案
    labels = pd.read_csv(
        str(data_path/"labels.csv"), index_col=0)
    # 將情緒情緒類別以one-hot encoding轉換
    one_hot_labels = pd.get_dummies(labels["label"])
    # 將filename和轉換欄位合併成一個DataFrame
    data = pd.concat([labels["filename"], one_hot_labels], axis=1)
    # print(f"labels.csv: {data}\n")
    categories = os.listdir(data_path)[1:]

    folder_dir = [train_dir, val_dir, test_dir]
    # 複製照片到train、val以及test資料夾(6:2:2)
    # 訓練集、驗證集、測試集比例
    train_ratio = 0.6
    val_ratio = 0.2
    test_ratio = 0.2
    for folder in folder_dir:
        for category in categories:
            sub_dir = os.path.join(folder, category)
            if not os.path.exists(sub_dir):
                os.makedirs(sub_dir)
    for category in categories:
        folder_path = os.path.join(data_path, category)
        filenames = os.listdir(folder_path)

        # 設置複製到train、val以及test的數量
        num_images = len(filenames)
        num_train = int(num_images * train_ratio)
        num_val = int(num_images * val_ratio)
        num_test = num_images - num_train - num_val

        # 複製的時候隨機選取檔案
        train_filenames = random.sample(filenames, num_train)
        val_filenames = random.sample(filenames[num_train:], num_val)
        test_filenames = random.sample(filenames[num_train+num_val:], num_test)

        # 複製檔案
        for filenames, dir in zip([train_filenames, val_filenames, test_filenames], folder_dir):
            for filename in filenames:
                original_dataset_path = os.path.join(
                    data_path, category, filename)
                base_path = os.path.join(dir, category)
                shutil.copy(original_dataset_path, base_path)


def extract_features(directory, sample_count):
    conv_base = VGG16(weights='imagenet',
                      include_top=False,             # 不包含 Full Connection
                      input_shape=(150, 150, 3))
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        # rotation_range=90,
        brightness_range=(0.5, 1),
        # shear_range=0.2,
        # zoom_range=0.2,
        channel_shift_range=0.2,
        horizontal_flip=False,
        vertical_flip=False,
        rescale=1./255,
        validation_split=0.3)
    features = np.zeros(shape=(sample_count, 4, 4, 512))
    labels = np.zeros(shape=(sample_count, 4))
    generator = datagen.flow_from_directory(
        directory,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='categorical')
    i = 0
    for inputs_batch, labels_batch in generator:
        features_batch = conv_base.predict(inputs_batch)
        features[i * batch_size: (i + 1) * batch_size] = features_batch
        labels[i * batch_size: (i + 1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count:
            break
    return features, labels


train_features, train_labels = extract_features(train_dir, 2400)
validation_features, validation_labels = extract_features(val_dir, 800)
test_features, test_labels = extract_features(test_dir, 800)

train_features = np.reshape(train_features, (2400, 4 * 4 * 512))
validation_features = np.reshape(validation_features, (800, 4 * 4 * 512))
test_features = np.reshape(test_features, (800, 4 * 4 * 512))
datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    # rotation_range=90,
    brightness_range=(0.5, 1),
    # shear_range=0.2,
    # zoom_range=0.2,
    channel_shift_range=0.2,
    horizontal_flip=False,
    vertical_flip=False,
    rescale=1./255,
    validation_split=0.3)
model = models.Sequential()
model.add(layers.Dense(256, activation='relu', input_dim=4 * 4 * 512))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(4, activation='softmax'))

model.compile(optimizer=optimizers.RMSprop(lr=2e-5),
              loss='categorical_crossentropy',
              metrics=['acc'])
history = model.fit(train_features, train_labels,
                    epochs=30,
                    batch_size=20,
                    validation_data=(validation_features, validation_labels))

# for folder in ['train', 'test', 'val']:
#     for category in os.listdir(data_path/'train'):
#         sub_dir = os.path.join(data_path/folder, category)
#         print(f"imgs in {folder} {category} {len(os.listdir(sub_dir))}")
model.save(Path(__file__).resolve().parent/'model/0504.h5')
with open(Path(__file__).resolve().parent/'model/0504.json', "w") as json_file:
    json.dump(history.history, json_file)
