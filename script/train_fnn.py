"""
This part is completed by Zeng Yucheng
Fully-connected neural network training and testing
"""

import numpy as np
from scipy.io import arff
import pandas as pd
from sklearn.model_selection import train_test_split
from keras import models, layers
import matplotlib.pyplot as plt
from keras.models import load_model

data = arff.loadarff('../datasets/Training Dataset.arff')
df = pd.DataFrame(data[0]).astype('int')
df = df[['URL_Length', 'Shortining_Service', 'having_At_Symbol', 'double_slash_redirecting', 'Prefix_Suffix',
         'Domain_registeration_length', 'Abnormal_URL', 'age_of_domain', 'URL_of_Anchor', 'SFH',
         'Submitting_to_email', 'Result']]
X = df.values[:, :-1]
df['one_hot_1'] = df['Result'].apply(lambda x: 1 if x == -1 else 0)
df['one_hot_2'] = df['one_hot_1'].apply((lambda x: 1 - x))
y = df.values[:, -2:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5331)

model = models.Sequential()
model.add(layers.Dense(16, activation='relu', input_shape=(X_train.shape[1],)))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(2, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=25, batch_size=512, validation_split=0.2)
history_dict = history.history
print(history_dict.keys())

loss_values = history_dict['loss']
val_loss_values = history_dict['val_loss']
epochs = range(1, len(loss_values) + 1)
plt.plot(epochs, loss_values, 'bo', label='Training loss')
plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

plt.clf()
acc_values = history_dict['accuracy']
val_acc_values = history_dict['val_accuracy']
plt.plot(epochs, acc_values, 'bo', label='Training acc')
plt.plot(epochs, val_acc_values, 'b', label='Validation acc')
plt.title('Training and validation accuracy')
plt.xlabel('Epochs')
plt.ylabel('Acc')
plt.legend()
plt.show()

# save and load model, first time only
# model.save('../models/fnn.m5')
# test_model = load_model('../models/fnn.m5')
# print(test_model.evaluate(X_test, y_test))


# ---------further analyze the ROC curve, AUC value and feature importance----------- #

