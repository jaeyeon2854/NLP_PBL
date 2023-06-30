from tqdm import tqdm
import re
from lyricscrawling import df

with open("../words/negative_words_self.txt", encoding='utf-8') as neg:
  negative = neg.readlines()

negative = [neg.replace("\n", "") for neg in negative]

with open("../words/positive_words_self.txt", encoding='utf-8') as pos:
  positive = pos.readlines()

negative = [neg.replace("\n", "") for neg in negative]
positive = [pos.replace("\n", "") for pos in positive]

labels = []

lyric_data = list(df['lyrics'])

for lyric in tqdm(lyric_data):
  clean_lyric = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》]', '', lyric) 
  negative_flag = False
  label = 0
  for i in range(len(negative)):
    if negative[i] in clean_lyric:
      label = -1
      negative_flag = True
      print("negative 비교단어 : ", negative[i], "clean_lyric : ", clean_lyric) 
      break
  if negative_flag == False:
    for i in range(len(positive)):
      if positive[i] in clean_lyric:
        label = 1
        print("positive 비교단어 : ", positive[i], "clean_lyric : ", clean_lyric)
        break

  labels.append(label)

df['label'] = labels

df.to_csv("new_lyrics_labeling.csv",  encoding='utf-8-sig')