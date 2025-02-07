import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer  # TF-IDF 벡터화를 위한 라이브러리
from scipy.io import mmwrite, mmread  # CSR 포맷의 행렬을 .mtx 파일로 저장하고 불러오는 라이브러리
import pickle  # 모델 저장을 위한 pickle 라이브러리

# CSV 파일에서 영화 리뷰 데이터를 불러옴
df_reviews = pd.read_csv('./crawlingdata/cleaned_reviews.csv')  # 'cleaned_reviews.csv' 파일에서 리뷰 데이터 불러오기
df_reviews.info()  # 데이터프레임 정보 출력 (열, 행 수, 데이터 타입 등)

# TF-IDF 벡터화 객체 생성
Tfidf = TfidfVectorizer(sublinear_tf=True)  # sublinear_tf=True: TF-IDF 값이 로그 변환된 형태로 계산됨
Tfidf_matrix = Tfidf.fit_transform(df_reviews.reviews)  # 리뷰 텍스트에 대해 TF-IDF 변환 적용
print(Tfidf_matrix.shape)  # TF-IDF 행렬의 크기 출력 (문서 수 x 단어 수)

# TF-IDF 모델을 pickle 파일로 저장
with open('./models/tfidf.pickle', 'wb') as f:  # TF-IDF 모델을 pickle 포맷으로 저장
    pickle.dump(Tfidf, f)  # 모델 객체를 pickle로 저장

# TF-IDF 행렬을 Matrix Market 형식으로 저장
mmwrite('./models/Tfidf_movie_review.mtx', Tfidf_matrix)  # .mtx 파일 형식으로 저장 (희소 행렬 형식)
