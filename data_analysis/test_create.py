import pandas as pd

#2022 train set
lyrics = pd.read_csv("../data/new_lyrics_labeling.csv")
df_lyric = lyrics[['lyrics', 'label']]
df_lyric

# new_lyrics.csv 후렴구 제거
df_lyric = df_lyric.drop([i for i in (543, 558)])
df_lyric = df_lyric.drop([1969,1970])
df_lyric = df_lyric.drop([i for i in (2302,2306)])
df_lyric = df_lyric.drop([i for i in (2621,2628)])
df_lyric = df_lyric.drop([i for i in (2667,2674)])
df_lyric = df_lyric.drop([3111,3112])
df_lyric

# 중복 행 제거
df_lyric = df_lyric.drop_duplicates()
df_lyric

# 한 글자만 있는 행 제거
for i in df_lyric['lyrics']:
  tmp = i.split(' ')
  if len(tmp) <= 1:
    df_lyric = df_lyric.drop(df_lyric[df_lyric['lyrics']==i].index)

df_lyric

# 시험 셋
df_lyric.to_csv("test.csv",  encoding='utf-8-sig')
