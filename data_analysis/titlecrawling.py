import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# 크롬 드라이버 연결
driver = webdriver.Chrome(executable_path="C:/Users/전기범/Desktop/NLP_PBL/chromedriver_win32/chromedriver.exe")

# 멜론 웹 페이지 접근
driver.get('https://www.melon.com/chart/index.htm')
driver.implicitly_wait(10)

# 제목 리스트
titles = [] 

def craw_title():
    # 제목 크롤링
    title = driver.find_element(By.CLASS_NAME,'song_name')
    titles.append(title.text)

    print(titles)

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
    craw_title()

# 데이터 프레임 생성
df = pd.DataFrame({"title": titles})

# csv 파일로 저장
df.to_csv("music_titles.csv",  encoding='utf-8-sig')
