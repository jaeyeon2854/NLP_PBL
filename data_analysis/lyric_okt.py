import pandas as pd
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
# DTM을 편리하게 만들어주기 위해 Scikit-Learn에서 제공하는 CountVectorizer를 import 한다.


if __name__ == '__main__':
    # 타이틀 리스트를 불러와서 lyric_list 변수에 저장한다.
    t_lyric_name = open('C:/Users/전기범/Desktop/NLP_PBL/data_analysis/lyric_list.txt', 'r', encoding='cp949')

    lyric_list = []
    for line in t_lyric_name.readlines():
        # txt파일을 readlines로 불러오면 개행 문자도 함께 읽어오기 때문에 인덱싱으로 처리해준다.
        lyric_list.append(line[:-1])

    t_lyric_name.close()

    # pandas의 read_csv 함수를 이용하여 csv 파일을 불러온다.
    dataset = pd.read_csv('C:/Users/전기범/Desktop/NLP_PBL/data/lyrics.csv')

    # 각 형태소별로 분류(Tagging)해주는 Okt 객체를 불러온다.
    tagger = Okt()

    for lyric in lyric_list:        # lyric_list에 대해 반복문을 실행
        # 각 타이틀에 대한 3191개 문서의 DTM을 표현하기 위해
        # CountVectorizer 객체를 선언
        cv = CountVectorizer()
        
        # 각 문서들의 말뭉치(corpus)를 저장할 리스트 선언
        corpus = []

        # 각 타이틀에 대한 문서들의 말 뭉치를 저장한다.
        for doc_num in range(3191):
            # 각 말뭉치에서 명사 리스트를 만든다.
            noun_list = tagger.nouns(dataset['lyric'].loc[doc_num])
            
            # 이를 문자열로 저장해야하기 때문에 join함수로 공백으로 구분해 corpus에 append한다.
            corpus.append(' '.join(noun_list))

        # CountVectorizer의 fit_transform 함수를 통해 DTM을 한번에 생성할 수 있다.
        DTM_Array = cv.fit_transform(corpus).toarray()

        # feature_names 함수를 사용하면 DTM의 각 열(column)이 어떤 단어에 해당하는지 알 수 있다.
        feature_names = cv.get_feature_names_out()

        # 추출해낸 데이터를 DataFrame 형식으로 변환한다.
        DTM_DataFrmae = pd.DataFrame(DTM_Array, columns=feature_names)

        # 최종적으로 DTM을 csv 파일로 저장한다.
        DTM_DataFrmae.to_csv('DTM4.csv', encoding='utf-8-sig')

        print(feature_names)
        print(cv.vocabulary_)