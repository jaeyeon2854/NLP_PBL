from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from konlpy.tag import Okt

#사용할 데이터 불러오기
music_lyrics = pd.read_csv("../data/lyrics.csv")
music_titles = pd.read_csv("../data/music_titles.csv")

##데이터 전처리
# 토크나이저 생성
tokenizer = Okt()

#가사,제목 데이터 가져옴
lyrics = music_lyrics['lyric']
titles = music_titles['title']

# 가사,제목 형태소 기준으로 토크나이징, 명사 형용사 부사만 추출
morph_lyrics = []
morph_titles = []

tmp_lyrics = []
tmp_titles = []

for lyric in lyrics:
  tmp = tokenizer.pos(lyric)
  tmp_lyrics.append(tmp)

for titles in titles:
  tmp = tokenizer.pos(titles)
  tmp_titles.append(tmp)

for i in tmp_lyrics:
  for word, tag in i:
    if tag in ['Noun', 'Adjective', 'Adverb'] and ("것" not in word) and ("수" not in word) and ("게" not in word):
      morph_lyrics.append(word)

for i in tmp_titles:
  for word, tag in i:
    if tag in ['Noun', 'Adjective', 'Adverb'] and ("것" not in word) and ("수" not in word) and ("게" not in word):
      morph_titles.append(word)

morph_lyrics = ' '.join(morph_lyrics)
morph_titles = ' '.join(morph_titles)

##워드클라우드
# word cloud 생성
wordcloud_lyrics = WordCloud(max_words=30, font_path='H2HDRM', max_font_size=100, background_color='white').generate(morph_lyrics)

wordcloud_titles = WordCloud(max_words=30, font_path='H2HDRM', max_font_size=100, background_color='white').generate(morph_titles)

# word cloud 가사 출력
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_lyrics, interpolation='lanczos')
plt.axis('off')
plt.show()

# word cloud 제목 출력
plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_titles, interpolation='lanczos')
plt.axis('off')
plt.show()