# 필요한 라이브러리와 모듈을 임포트합니다.
import sys  # 시스템 관련 기능을 위한 라이브러리
from audioop import reverse

from PyQt5.QtWidgets import *  # PyQt5의 위젯 관련 클래스들
from PyQt5 import uic  # .ui 파일을 로드하기 위한 모듈
import pandas as pd  # 데이터 처리용 라이브러리
from pandas.core.config_init import use_inf_as_na_cb  # 판다스 관련 (이 코드에서 사용되지 않음)
from sklearn.metrics.pairwise import linear_kernel  # 코사인 유사도 계산을 위한 함수 (추천 시스템 관련)
from gensim.models import Word2Vec  # 자연어 처리용 Word2Vec 모델
from scipy.io import mmread  # 희소 행렬을 읽어오는 함수 (추천 시스템 관련)
import pickle  # 모델이나 데이터를 직렬화/역직렬화하는 모듈
from PyQt5.QtCore import QStringListModel  # QStringListModel을 위한 모듈 (리스트 모델 관련)

from job06_recommendation import recommendation

# .ui 파일을 로드하여 Python 클래스 형태로 변환합니다.
from_window = uic.loadUiType('C:/work/movie_for_you_inel03/movie_recommendation.ui')[0]

# UI를 연결한 클래스 정의
class Exam(QWidget, from_window):

    def __init__(self):
        super().__init__()  # 부모 클래스(QWidget)의 초기화 호출
        self.setupUi(self)  # UI 구성 요소를 초기화합니다.
        self.Tfidf_matrix = mmread('C:/work/movie_for_you_inel03/models/Tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle','rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('C:/work/movie_for_you_inel03/models/word2vec_movie_review.model')

        self.df_reviews = pd.read_csv('C:/work/movie_for_you_inel03/crawlingdata/cleaned_reviews.csv')
        self.titles = list(self.df_reviews.titles)
        self.titles.sort()
        for title in self.titles:
            self.cb_title.addItem(title)

        model = QStringListModel()
        model.setStringList((self.titles))
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)

        self.cb_title.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommend.clicked.connect(self.btn_slot)

    def btn_slot(self):
        keyword = self.le_keyword.text()
        if keyword in self.titles:
            recommendation = self.recommendation_by_title(keyword)
        else:
            recommendation = self.recommendation_by_keyword(keyword)
        if(recommendation):
            self.lbl_recommendation.setText(recommendation)

    def combobox_slot(self):
        title = self.cb_title.currentText()
        print(title)
        recommendation = self.recommendatation_by_title(title)
        self.lbl_recommendation.setText(recommendation)

    def recommendation_by_title(self, title):
        movie_idx = self.df_reviews[self.df_reviews.titles == title].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation))
        return recommendation

    def recommendation_by_keyword(self, keyword):
        try:
            sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
        except:
            self.lbl_recommendation.setText('제가 모르는 단어에요 ㅜㅜ')
            return 0



        words = [keyword]
        for word, _ in sim_word:
            words.append(word)
        print(words)
        sentence=[]
        count = 10
        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        print(sentence)
        sentence_vec = self.Tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(recommendation)
        return  recommendation




    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)
        simScore = simScore[:11]
        movieIdx = [i[0] for i in simScore]
        recmovieList = self.df_reviews.iloc[movieIdx,0]
        return recmovieList[1:11]

# 프로그램 시작 부분
if __name__ == '__main__':  # 이 파일이 직접 실행될 경우
    app = QApplication(sys.argv)  # Qt 애플리케이션 객체 생성
    mainWindow = Exam()  # Exam 클래스의 인스턴스를 생성하여 메인 윈도우로 설정
    mainWindow.show()  # 윈도우를 화면에 띄움
    sys.exit(app.exec_())  # 애플리케이션 실행, 종료 시 시스템 종료 코드 반환