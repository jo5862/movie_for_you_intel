from itertools import count

import pandas as pd  # 데이터 처리 및 분석을 위한 라이브러리
from sklearn.metrics.pairwise import linear_kernel  # 코사인 유사도를 계산하기 위한 함수
from scipy.io import mmread  # Matrix Market 형식의 파일을 읽어오는 함수
import pickle  # Python 객체를 저장하거나 불러오기 위한 라이브러리
from konlpy.tag import Okt  # 한국어 형태소 분석을 위한 라이브러리 (이 코드에서는 사용되지 않음)
from gensim.models import Word2Vec  # Word2Vec 모델을 위한 라이브러리 (이 코드에서는 사용되지 않음)


# 영화 추천 함수 정의
def getRecommendation(cosine_sim):
    # 코사인 유사도가 가장 높은 영화들의 인덱스를 추출하여 추천 영화 리스트를 반환
    simScore = list(enumerate(cosine_sim[-1]))  # 주어진 영화와 다른 영화들 간의 유사도를 나열합니다.
    simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 유사도 순으로 정렬합니다.
    simScore = simScore[:11]  # 가장 유사한 10개 영화(자기 자신 제외)를 선택합니다.
    movieIdx = [i[0] for i in simScore]  # 유사도 높은 영화들의 인덱스를 추출합니다.
    recmovieList = df_reviews.iloc[movieIdx, 0]  # 인덱스를 이용해 영화 제목을 추출합니다.
    return recmovieList[1:11]  # 추천 영화 리스트를 반환합니다. (자기 자신은 제외)

# 데이터 불러오기 및 TF-IDF 모델 로드
df_reviews = pd.read_csv('./crawlingdata/cleaned_reviews.csv')  # 영화 리뷰 데이터가 들어 있는 CSV 파일을 불러옵니다.
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()  # Matrix Market 형식으로 저장된 TF-IDF 행렬을 읽어옵니다.
with open('./models/tfidf.pickle', 'rb') as f:  # pickle 파일로 저장된 TF-IDF 모델을 불러옵니다.
    Tfidf = pickle.load(f)  # 모델을 로드합니다.
#
# # 영화 인덱스 설정 (추천할 영화 기준)
# ref_idx = 349  # 추천 기준이 될 영화의 인덱스를 설정합니다.
# print('title', df_reviews.iloc[ref_idx, 0])  # 기준 영화의 제목을 출력합니다.
#
# # 코사인 유사도 계산 (기준 영화와 다른 영화들 간의 유사도)
# cosine_sim = linear_kernel(Tfidf_matrix[ref_idx], Tfidf_matrix)  # 코사인 유사도 계산
#
# # 코사인 유사도 및 추천 영화 출력
# print(cosine_sim[0])  # 기준 영화와 다른 영화들 간의 유사도 출력
# print(len(cosine_sim[0]))  # 유사도 배열의 길이 출력 (영화의 개수)
#
# # # 추천 영화 리스트 얻기
# # recommendations = getRecommendation(cosine_sim)  # 추천 영화 리스트를 반환받습니다.
# # print(recommendations)  # 추천된 영화 제목 출력

#KEY WORD이용
embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')
keyword ='엄마'
if keyword in list(embedding_model.wv.index_to_key):
    sim_word = embedding_model.wv.most_similar(keyword,topn=10)
    words = [keyword]
    for word, _ in sim_word:
        words.append(word)
    print(words)
else :
    print('not in')
sentence = []
count = 10
for word in words:
    sentence = sentence + [word] *count
    count -= 1
sentence = ' '.join(sentence)
print(sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim =linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)

print(recommendation)
# df_reviews.info()  # 데이터프레임의 정보를 출력할 수 있습니다. (주석 처리된 부분)
