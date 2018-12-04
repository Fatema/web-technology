import pandas as pd
import numpy as np

class RecommendationSystem:
    def __init__(self):
        self.movies = pd.read_csv('data/movies.csv')
        self.ratings = pd.read_csv('ml-latest-small/ratings.csv')

        self.movie_data = pd.merge(self.ratings, self.movies, on='movieId')

        self.movies['year'] = self.movies['title']\
            .str.extract(r'\((\d{4})\)', expand=False)\
            .astype('float64').fillna(0).astype('int64')

        self.genres = set(self.movies['genres'].str.cat(sep='|').split('|'))

        self.ratings_mean_count = pd.DataFrame(self.movie_data.groupby('movieId')['rating'].mean())
        self.ratings_mean_count['rating_counts'] = pd.DataFrame(self.movie_data.groupby('movieId')['rating'].count())

        self.user_movie_rating = self.movie_data.pivot_table(index='userId', columns='movieId', values='rating')

    def recommendation_ratings_correlation(self, movie_id):
        movie_ratings = self.user_movie_rating[movie_id]

        similar_movies = self.user_movie_rating.corrwith(movie_ratings)

        corr_movie = pd.DataFrame(similar_movies, columns=['Correlation'])
        corr_movie.dropna(inplace=True)
        corr_movie.sort_values('Correlation', ascending=False)
        corr_movie = corr_movie.join(self.ratings_mean_count['rating_counts'])
        corr_movie[corr_movie['rating_counts'] > 50].sort_values('Correlation', ascending=False)
