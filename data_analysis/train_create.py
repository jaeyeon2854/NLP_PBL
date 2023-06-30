import pandas as pd

#lyrics.csv test set
lyrics = pd.read_csv("../data/lyrics.csv")
df_lyric = lyrics[['lyric', 'label']]
df_lyric

#lyrics.csv 후렴구 제거
df_lyric = df_lyric.drop([i for i in (369, 384)])
df_lyric = df_lyric.drop([1280,1282])
df_lyric = df_lyric.drop([1299, 1300])
df_lyric = df_lyric.drop([i for i in (1865,1870)])
df_lyric = df_lyric.drop([2831, 2832])
df_lyric


# 중복 행 제거
df_lyric = df_lyric.drop_duplicates()
df_lyric

# 한 글자만 있는 행 제거
for i in df_lyric['lyric']:
  tmp = i.split(' ')
  if len(tmp) <= 1:
    df_lyric = df_lyric.drop(df_lyric[df_lyric['lyric']==i].index)

df_lyric

df_lyric.to_csv("train.csv",  encoding='utf-8-sig')

