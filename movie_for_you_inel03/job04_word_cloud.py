import pandas as pd
from wordcloud import WordCloud
import collections
import matplotlib.pyplot as plt
from matplotlib import font_manager

# 한글 폰트 경로 설정
font_path = './malgun.ttf'  # 사용할 한글 폰트 경로
font_name = font_manager.FontProperties(fname=font_path).get_name()  # 폰트 이름 추출
plt.rc('font', family='NanumBrunGothic')  # 전체 Matplotlib에서 사용할 폰트 설정

# CSV 파일을 읽어들여 데이터프레임으로 로드
df = pd.read_csv('./crawlingdata/cleaned_reviews.csv')  # 리뷰 데이터가 있는 CSV 파일을 읽어옴

# 특정 행과 열을 선택하여 단어들을 리스트로 분리
words = df.iloc[349, 1].split()  # 349번째 행의 두 번째 열에서 리뷰 텍스트를 공백으로 분리하여 리스트로 저장

# 선택한 영화(리뷰)의 제목 출력
print(df.iloc[349, 0])  # 349번째 행의 첫 번째 열에 있는 영화 제목 출력

# 단어 빈도 계산
worddict = collections.Counter(words)  # 리스트에 있는 단어들의 빈도수를 세어서 dict 형식으로 저장
worddict = dict(worddict)  # Counter 객체를 일반 dict로 변환
print(worddict)  # 단어 빈도 출력

# 워드클라우드 생성
wordcloud_img = WordCloud(
    background_color='white',  # 배경색은 흰색
    font_path=font_path  # 한글 폰트 설정
).generate_from_frequencies(worddict)  # 단어 빈도수를 기반으로 워드클라우드 생성

# 워드클라우드를 화면에 출력
plt.figure(figsize=(12, 12))  # 워드클라우드 이미지 크기 설정
plt.imshow(wordcloud_img, interpolation='bilinear')  # 워드클라우드 이미지를 화면에 표시
plt.axis('off')  # 축을 표시하지 않음
plt.show()  # 워드클라우드 이미지를 화면에 표시
