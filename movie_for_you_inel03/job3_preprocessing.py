import pandas as pd
from konlpy.tag import Okt  # 한국어 형태소 분석을 위한 konlpy 라이브러리의 Okt 모듈 사용
import re  # 정규표현식 라이브러리

# 데이터를 불러옴 (영화 리뷰 데이터를 포함하는 CSV 파일)
df = pd.read_csv('./crawlingdata/reviews_kinolights.csv')
df.info()  # 데이터프레임 정보 출력

# 불용어 목록을 불러옴
df_stopwords = pd.read_csv('./crawlingdata/stopwords (1).csv')
stopwords = list(df_stopwords['stopword'])  # 불용어 리스트로 변환
# print(stopwords)  # 불용어 출력 (디버깅용 주석)

okt = Okt()  # Okt 객체 생성
print(df.titles[0])  # 첫 번째 영화 제목 출력 (디버깅용 주석)
print(df.reviews[0])  # 첫 번째 영화 리뷰 출력 (디버깅용 주석)

cleaned_sentences = []  # 정제된 문장을 저장할 리스트 초기화

# 각 리뷰에 대해 반복하여 처리
for review in df.reviews:
    review = re.sub('[^가-힣]', ' ', review)  # 한글과 공백을 제외한 모든 문자를 제거
    print(review)  # 정제된 리뷰 출력 (디버깅용 주석)

    # Okt를 사용하여 형태소 분석 (어간 추출 포함)
    tokened_review = okt.pos(review, stem=True)
    print(tokened_review)  # 형태소 분석 결과 출력 (디버깅용 주석)

    # 형태소 분석 결과를 DataFrame으로 변환
    df_token = pd.DataFrame(tokened_review, columns=['word', 'class'])

    # 명사, 동사, 형용사만 필터링
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]
    print(df_token)  # 필터링된 형태소 출력 (디버깅용 주석)

    words = []  # 필터링된 단어를 저장할 리스트 초기화
    for word in df_token.word:
        if 1 < len(word):  # 길이가 1보다 큰 단어만 선택
            if word not in stopwords:  # 불용어 목록에 없는 단어만 선택
                words.append(word)  # 단어를 리스트에 추가

    cleaned_sentence = ' '.join(words)  # 단어들을 공백으로 구분하여 하나의 문장으로 결합
    cleaned_sentences.append(cleaned_sentence)  # 정제된 문장을 리스트에 추가

# 정제된 문장을 데이터프레임의 reviews 컬럼에 할당
df.reviews = cleaned_sentences

# 결측치가 있는 행 삭제
df.dropna(inplace=True)

# 데이터프레임 정보 출력
df.info()

# 정제된 데이터를 새로운 CSV 파일로 저장
df.to_csv('./crawlingdata/cleaned_reviews.csv', index=False)

# 마지막 정제된 문장 출력 (디버깅용 주석)
print(cleaned_sentence)
