import pandas as pd
import glob

# 'movie_reviews_500_movies' 폴더 안의 모든 CSV 파일 경로를 가져옴
data_paths = glob.glob('./crawlingdata/movie_reviews_500_movies/*')
print(data_paths)  # 파일 경로 출력

# 새로운 빈 DataFrame 생성
df = pd.DataFrame()

# 각 파일에 대해 반복 처리
for path in data_paths:
    # 각 파일을 읽어오기
    df_temp = pd.read_csv(path)  # 현재 파일을 pandas DataFrame으로 읽어오기
    print(df_temp.head())  # 해당 파일의 첫 5개 행 출력 (확인용)

    titles = []  # 제목을 저장할 리스트
    reviews = []  # 리뷰를 저장할 리스트
    old_title = ''  # 이전 제목을 저장하기 위한 변수 (초기값은 빈 문자열)

    # 각 행을 순차적으로 처리
    for i in range(len(df_temp)):
        title = df_temp.iloc[i, 0]  # 제목 열에서 값 추출 (0번째 열)

        # 제목이 이전 제목과 다르면 제목을 추가
        if title != old_title:
            title = title.replace('"', '')  # 제목에서 불필요한 따옴표 제거
            titles.append(title)  # 제목 리스트에 제목 추가
            old_title = title  # 이전 제목을 현재 제목으로 업데이트

            # 같은 제목을 가진 리뷰들을 하나로 합침
            df_movie = df_temp[df_temp.movie_title == title]  # 동일 제목의 데이터만 추출
            review = ' '.join(df_movie.review)  # 해당 제목의 리뷰들을 공백으로 구분하여 합침
            reviews.append(review)  # 리뷰 리스트에 합친 리뷰 추가

    # 제목과 리뷰 리스트의 길이 출력 (확인용)
    print(len(titles))
    print(len(reviews))

    # 새로운 데이터프레임 배치 생성
    df_batch = pd.DataFrame({'titles': titles, 'reviews': reviews})  # 제목과 리뷰 리스트로 데이터프레임 생성
    df_batch.info()  # 데이터프레임 정보 출력 (각 열의 데이터 타입, 행 개수 등)
    print(df_batch)  # 데이터프레임의 내용 출력 (확인용)

    # 기존 데이터프레임에 새로운 배치 합치기
    df = pd.concat([df, df_batch], ignore_index=True)  # df_batch를 기존 df에 병합

# 최종 데이터프레임 정보 출력
df.info()  # 전체 데이터프레임의 정보 출력
# 최종 데이터프레임을 CSV 파일로 저장
df.to_csv('./crawlingdata/reviews_kinolights.csv', index=False)  # 파일로 저장 (인덱스 제외)
