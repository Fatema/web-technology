import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds


class RecommendationEngine:
    def __init__(self):
        self.movies = pd.read_csv('data/movies.csv')
        self.ratings = pd.read_csv('data/ratings.csv')
        self.update_movie_data()

    def update_movie_data(self):
        self.movie_data = pd.merge(self.ratings, self.movies, on='movieId')

        self.movies['year'] = self.movies['title']\
            .str.extract(r'\((\d{4})\)', expand=False)\
            .astype('float64').fillna(0).astype('int64')

        self.genres = set(self.movies['genres'].str.cat(sep='|').split('|'))

        self.ratings_mean_count = pd.DataFrame(self.movie_data.groupby('movieId')['rating'].mean())
        self.ratings_mean_count['rating_counts'] = pd.DataFrame(self.movie_data.groupby('movieId')['rating'].count())

        self.user_movie_rating = self.ratings.pivot_table(index='userId', columns='movieId', values='rating').fillna(0)

        self.R = self.user_movie_rating.values
        self.user_ratings_mean = np.mean(self.R, axis=1)
        self.R_demeaned = self.R - self.user_ratings_mean.reshape(-1, 1)
        self.U, self.sigma, self.Vt = svds(self.R_demeaned, k=50)
        self.sigma = np.diag(self.sigma)

        self.all_user_predicted_ratings = np.dot(np.dot(self.U, self.sigma), self.Vt) + self.user_ratings_mean.reshape(-1, 1)
        self.preds = pd.DataFrame(self.all_user_predicted_ratings, columns=self.user_movie_rating.columns)

    def update_ratings(self, user_id, movie_id, rating):
        timestamp = (pd.datetime.now() - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
        df = pd.DataFrame({'userId': [user_id], 'movieId': [movie_id], 'rating': [rating], 'timestamp': [timestamp]})

        user_ratings = self.ratings[self.ratings['userId'] == user_id]
        movie_rated = user_ratings[user_ratings['movieId'] == movie_id]

        if user_ratings.empty or movie_rated.empty:
            self.ratings.append(df, ignore_index=True)
            with open('data/ratings.csv', 'a') as f:
                df.to_csv(f, header=False)
        else:
           self.ratings.loc[(self.ratings['userId'] == user_id) & (self.ratings['movieId'] == movie_id), 'rating'] = rating
           self.ratings.loc[(self.ratings['userId'] == user_id) & (self.ratings['movieId'] == movie_id), 'timestamp'] = timestamp
           with open('data/ratings.csv', 'w') as f:
               self.ratings.to_csv(f, header=True)

        self.update_movie_data()

    def recommendation_ratings_correlation(self, movie_id, num_recommendations=5):
        movie_ratings = self.user_movie_rating[movie_id]

        similar_movies = self.user_movie_rating.corrwith(movie_ratings)

        corr_movie = pd.DataFrame(similar_movies, columns=['Correlation'])
        corr_movie.dropna(inplace=True)
        corr_movie.sort_values('Correlation', ascending=False)
        corr_movie = corr_movie.join(self.ratings_mean_count['rating_counts'])

        # get top ten movies than have at least 50 ratings
        corr_movie_top10 = (corr_movie[corr_movie['rating_counts'] > 50].
                                sort_values('Correlation', ascending=False).
                                iloc[:num_recommendations, :-1])

        recommendations = pd.merge(self.movies, corr_movie_top10, how = 'inner')

        return recommendations

    def recommendation_ratings_matrix_factorization(self, user_id, num_recommendations=5):
        # Get and sort the user's predictions
        user_row_number = user_id - 1  # UserId starts at 1, not 0
        sorted_user_predictions = self.preds.iloc[user_row_number].sort_values(ascending=False)

        # Get the user's data and merge in the movie information.
        user_data = self.ratings[self.ratings.userId == user_id]
        user_full = (user_data.merge(self.movies, how='left', left_on='movieId', right_on='movieId')
            .sort_values(['rating'], ascending=False))

        # Recommend the highest predicted rating movies that the user hasn't seen yet.
        recommendations = (self.movies[~self.movies['movieId'].isin(user_full['movieId'])].
                               merge(pd.DataFrame(sorted_user_predictions).reset_index(),
                                     how='left',
                                     left_on='movieId',
                                     right_on='movieId').
                               rename(columns={user_row_number: 'Predictions'}).
                               sort_values('Predictions', ascending=False).
                               iloc[:num_recommendations, :-1])

        return user_full, recommendations
