'''
Author: Withoutwaxwqy 2137697992@qq.com
Date: 2025-02-06 13:50:07
LastEditors: Withoutwaxwqy 2137697992@qq.com
LastEditTime: 2025-02-07 10:05:37
FilePath: \GNSSutils\deepFusion\deeptest.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import tensorflow as tf
from tensorflow.keras import layers, models # type: ignore
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger # type: ignore
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 假设数据保存在 CSV 文件中
data = pd.read_csv(r'D:\private projections\GNSSutils\data\deepLtest\data.csv')


# 设置环境变量以使用 8 个 CPU 内核
os.environ["OMP_NUM_THREADS"] = "8"
os.environ["TF_NUM_INTRAOP_THREADS"] = "8"
os.environ["TF_NUM_INTEROP_THREADS"] = "8"

# 配置 TensorFlow 使用 8 个 CPU 内核
tf.config.threading.set_intra_op_parallelism_threads(8)
tf.config.threading.set_inter_op_parallelism_threads(8)


# 提取特征和标签
features = data[['A', 'B', 'C', 'D', 'E']].values
labels = data['scene'].values

# 对标签进行编码
label_encoder = LabelEncoder()
labels = label_encoder.fit_transform(labels)

# 将数据划分为训练集和测试集
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.2, random_state=42)

# 将数据转换为适合 CNN 输入的格式
train_features = train_features.reshape((train_features.shape[0], 5, 1, 1)).astype('float32')
test_features = test_features.reshape((test_features.shape[0], 5, 1, 1)).astype('float32')



# 构建模型
model = models.Sequential()
model.add(layers.Conv2D(32, (2, 1), activation='relu', input_shape=(5, 1, 1)))
model.add(layers.MaxPooling2D((2, 1)))
model.add(layers.Conv2D(64, (2, 1), activation='relu'))
model.add(layers.GlobalAveragePooling2D())
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(len(np.unique(labels)), activation='softmax'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(len(np.unique(labels)), activation='softmax'))

# 查看模型架构
model.summary()

# 编译模型
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

# 设置回调函数
checkpoint_cb = ModelCheckpoint('model_weights.h5', save_best_only=True)
csv_logger_cb = CSVLogger('training_log.csv')

# 训练模型
history = model.fit(train_features, train_labels, epochs=2, 
                    validation_data=(test_features, test_labels),
                    callbacks=[checkpoint_cb, csv_logger_cb])

# 评估模型
test_loss, test_acc = model.evaluate(test_features, test_labels, verbose=2)
print(f'\nTest accuracy: {test_acc}')

# 保存模型
os.makedirs('model', exist_ok=True)
model.save('model')

# 绘制训练结果
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label = 'val_accuracy')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.ylim([0, 1])
plt.legend(loc='lower right')
plt.show()