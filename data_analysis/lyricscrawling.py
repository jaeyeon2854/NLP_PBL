import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

##labeling X
# 크롬 드라이버 연결
driver = webdriver.Chrome(executable_path="C:/Users/전기범/Desktop/NLP_PBL/chromedriver_win32/chromedriver.exe")

# 멜론 웹 페이지 접근
driver.get('https://www.melon.com/chart/index.htm')
driver.implicitly_wait(10)

# 모든 노래들을 모으는 리스트
all_lyrics=[]
#  가사정보,제목 크롤링 함수
def lyrics_crawling():
    lyric = driver.find_elements(By.CLASS_NAME,'lyric')
    driver.implicitly_wait(10)

    lyrics = []

    lyrics = lyric[0].text.split('\n')

    # 공백 제거
    lyrics = list(filter(None, lyrics))

    # 영어 제거
    lyrics = list(filter(lambda i: i.upper() == i.lower(), lyrics))

    for i in lyrics:
        all_lyrics.append(i)
    

# data-song-no를 모으는 리스트
song_num = []

lst50 = driver.find_elements(By.ID,'lst50')
lst100 = driver.find_elements(By.ID,'lst100')
for i in lst50:
    song_num.append(i.get_attribute('data-song-no'))
for i in lst100:
    song_num.append(i.get_attribute('data-song-no'))

# 상세 페이지 접근
for i in range(100):
    driver.get('https://www.melon.com/song/detail.htm?songId={song_num}'.format(song_num=song_num[i]))
    lyrics_crawling()


# 데이터 프레임 생성

df = pd.DataFrame({"lyrics": all_lyrics, "label":0})

# csv 파일로 저장
df.to_csv("new_lyrics.csv",  encoding='utf-8-sig')