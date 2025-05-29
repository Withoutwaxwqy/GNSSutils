import os
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import sys

def readMultiCsv(fp):
    """
    READ MULTI CSV
    files: list
    return: list
    """
    rfile = os.listdir(fp)
    files = [os.path.join(fp, f) for f in rfile]

    data_frames = [pd.read_csv(file) for file in files]
    out = pd.concat(data_frames)
    return out
# 假设数据保存在 CSV 文件中



data = readMultiCsv(r'D:\private projections\GNSSutils\data\deepLtest\gnssTFtest')



# 设置环境变量以使用 8 个 CPU 内核
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["TF_NUM_INTRAOP_THREADS"] = "8"
os.environ["TF_NUM_INTEROP_THREADS"] = "8"

# 配置 TensorFlow 使用 8 个 CPU 内核
tf.config.threading.set_intra_op_parallelism_threads(8)
tf.config.threading.set_inter_op_parallelism_threads(8)

# 提取特征和标签
sceneindex = ["cycleSlipratio","average CN0","average Elevation","vis satellite number","hDop","pDop","ValidLNum","aveEleOfValid"]
features = data[sceneindex].values
labels = data['scene'].values

# 对标签进行编码
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# 将数据划分为训练集和测试集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2, random_state=42)

# 将数据转换为适合 CNN 输入的格式
train_features = train_features.reshape((train_features.shape[0], 8, 1, 1)).astype('float32')
test_features = test_features.reshape((test_features.shape[0], 8, 1, 1)).astype('float32')

# 构建模型
# model = models.Sequential()
# model.add(layers.Conv2D(32, (3, 1), activation='relu', input_shape=(8, 1, 1)))
# model.add(layers.MaxPooling2D((2, 1)))
# model.add(layers.Conv2D(64, (3, 1), activation='relu'))
# model.add(layers.GlobalAveragePooling2D())
# model.add(layers.Flatten())
# model.add(layers.Dense(128, activation='relu'))
# model.add(layers.Dropout(0.5))
# model.add(layers.Dense(64, activation='relu'))
# model.add(layers.Dropout(0.5))
# model.add(layers.Dense(len(np.unique(labels)), activation='softmax'))
model = models.Sequential()
model.add(layers.Conv1D(32, 3, activation='relu', input_shape=(8, 1)))
model.add(layers.MaxPooling1D(2))
model.add(layers.Conv1D(64, 3, activation='relu'))
model.add(layers.GlobalAveragePooling1D())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(len(np.unique(labels)), activation='softmax'))
# 查看模型架构
model.summary()

# 编译模型
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 设置回调函数
checkpoint_cb = ModelCheckpoint('model_weights.h5', save_best_only=True)
csv_logger_cb = CSVLogger('training_log.csv')

# 训练模型
history = model.fit(train_features, train_labels, epochs=30, 
                    validation_data=(test_features, test_labels),
                    callbacks=[checkpoint_cb, csv_logger_cb])

# 评估模型
test_loss, test_acc = model.evaluate(test_features, test_labels, verbose=2)
print(f'\nTest accuracy: {test_acc}')

# 保存模型
os.makedirs('model', exist_ok=True)
model.save('model/model.h5')

# 绘制训练结果
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()