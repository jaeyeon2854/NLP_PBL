from __future__ import annotations
from keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, Embedding, LSTM
from keras.callbacks import EarlyStopping
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from keras.utils import pad_sequences

# 토크나이저 생성
tokenizer = Okt()

train_data = pd.read_csv("../data/train.csv")
test_data = pd.read_csv("../data/test.csv")
title_name=pd.read_csv("../data/music_info.csv")

train_data['label'].value_counts().plot(kind='bar')
plt.show()
test_data['label'].value_counts().plot(kind='bar')
plt.show()

print(train_data.groupby('label').size().reset_index(name='count'))
print(test_data.groupby('label').size().reset_index(name='count'))

file_path="C:/Users/전기범/Desktop/NLP_PBL/words/stopwords-ko.txt"

with open(file_path,encoding='utf-8') as f:
  lines = f.readlines()
lines = [line.rstrip('\n') for line in lines]

stopwords = lines

okt = Okt()
X_train = []
for lyrics in train_data['lyric']:
  temp_X = []
  temp_X = okt.morphs(lyrics, stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  X_train.append(temp_X)

  
X_test = []
for lyrics in test_data['lyrics']:
  temp_X = []
  temp_X = okt.morphs(lyrics, stem=True) # 토큰화
  temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
  X_test.append(temp_X)

print(X_train[100:103])
print(X_test[100:103])

max_words = 35000
tokenizer = Tokenizer(num_words = max_words)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test) 
print(X_train[100:103])
print(X_test[100:103])


print("가사의 최대 길이 : ", max(len(l) for l in X_train))
print("가사의 평균 길이 : ", sum(map(len, X_train))/ len(X_train))
plt.hist([len(s) for s in X_train], bins=50)
plt.xlabel('length of Data')
plt.ylabel('number of Data')
plt.show()

print("가사의 최대 길이 : ", max(len(l) for l in X_test))
print("가사의 평균 길이 : ", sum(map(len, X_test))/ len(X_test))
plt.hist([len(s) for s in X_test], bins=50)
plt.xlabel('length of Data')
plt.ylabel('number of Data')
plt.show()

y_train = []
y_test = []

for i in range(len(train_data['label'])):
  if train_data['label'].iloc[i] == 1:
    y_train.append([0, 0, 1])
  elif train_data['label'].iloc[i] == 0:
    y_train.append([0, 1, 0])
  elif train_data['label'].iloc[i] == -1:
    y_train.append([1, 0, 0])

for i in range(len(test_data['label'])):
  if test_data['label'].iloc[i] == 1:
    y_test.append([0, 0, 1])
  elif test_data['label'].iloc[i] == 0:
    y_test.append([0, 1, 0])
  elif test_data['label'].iloc[i] == -1:
    y_test.append([1, 0, 0])

y_train = np.array(y_train)
y_test = np.array(y_test)

print(y_train[100:103])
print(y_test[100:103])

max_len = 16 # 전체 데이터의 길이를 16로 맞춘다

X_train = pad_sequences(X_train, maxlen=max_len)
X_test = pad_sequences(X_test, maxlen=max_len)

model = Sequential()
model.add(Embedding(max_words, 100))
model.add(LSTM(128,recurrent_dropout=0.2))
model.add(Dense(3, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

early_stopping = EarlyStopping(monitor='val_loss', mode='min', verbose=1, patience=3)

history = model.fit(X_train, y_train, epochs=20,validation_split=0.2,callbacks = [early_stopping])

print("\n 테스트 정확도 : {:.2f}%".format(model.evaluate(X_test,y_test)[1]*100))
predict = model.predict(X_test)

predict_labels = np.argmax(predict, axis=1)
original_labels = np.argmax(y_test, axis=1)

for i in range(100):
  print("가사 : ", test_data['lyrics'].iloc[i], "/\t 원래 라벨 : ", original_labels[i], "/\t예측한 라벨 : ", predict_labels[i])

def divide_list(l, n): 
    # 리스트 l의 길이가 n이면 계속 반복
    for i in range(0, len(l)-3, n): 
        yield l[i:i + n] 
# 한 리스트에 몇개씩 담을지 결정
n = 36
result = list(divide_list(predict_labels, n))

def make_val ():
  b=[]
  for val in result:
    a=np.sum(val)
    if a > 40:
      b.append('긍정 노래입니다.')
    elif a < 40 :
      b.append('부정 노래입니다.')
    else:
      b.append('중립 노래입니다.')
  for i in range(100):
    print("제목 : ", title_name['titles'].iloc[i], "/\t예측한 결과 : ", b[i])

make_val()

plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], 'b-', label='loss')
plt.plot(history.history['val_loss'], 'r--', label='val_loss')
plt.xlabel('Epoch')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], 'g-', label='accuracy')
plt.plot(history.history['val_accuracy'], 'k--', label='val_accuracy')
plt.xlabel('Epoch')
plt.ylim(0, 1)
plt.legend()

plt.show()

