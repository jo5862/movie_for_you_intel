import pandas as pd

df = pd.read_csv('crawlingdata/movie_400_20250204_combine.csv')
df.dropna(inplace=True)
df.info()
print(df.head())
print(df.columns)

titles=[]
reviews = []
old_title = ''
for i in range(len(df)):
        title = df.iloc[i,0]
        if title != old_title:
            titles.append(title)
            old_title =title
            df_movie = df[df['Title'] == title]  # 열 이름을 'Title'로 변경
            review = ' '.join(df_movie['Review'])  # 여기서 'Review'가 올바른 열 이름이라고 가정
            reviews.append(review)
print(len(titles))
print(len(reviews))
df= pd.DataFrame({'titles': titles, 'reviews':reviews})
df.info()
print(df)
df.to_csv('./crawlingdata/reviews_kinolights_1.csv', index = False)