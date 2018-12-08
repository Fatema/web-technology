from flask import json
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

from recommendation_engine import RecommendationEngine

class Service:

    def __init__(self):
        self.r_engine = RecommendationEngine()

        # all this information shouldn't be part of the api but for the sake of this assignment it is here
        self.users = pd.read_csv('data/users.csv')
        self.search_words = pd.read_csv('data/search_words.csv')
        self.search_genres = pd.read_csv('data/search_genres.csv')
        self.search_ratings = pd.read_csv('data/search_ratings.csv')
        self.search_years = pd.read_csv('data/search_years.csv')
        self.preferred_genres = pd.read_csv('data/preferred_genres.csv')
        self.movie_clicks = pd.read_csv('data/clicks.csv')

        self.num_users = self.users.shape[0]
        self.last_id = self.users['userId'].max()

        self.user_id = None
        self.set_user_profile()

        self.last_movie_clicked = None

        self.empty = pd.DataFrame()

        self.movies_list = self.empty
        self.recommendations = self.empty
        self.user_ratings = self.empty

        self.stop_words = set(stopwords.words('english'))

    def login(self, username, password):
        user = self.users[(self.users['username'] == username) & (self.users['password'] == password)]
        if not user.empty:
            self.user_id = user.iloc[0]['userId']
            self.set_user_profile()
            return True
        return False

    def get_user_static_data(self):
        print(self.user_id)
        user = self.users[self.users['userId'] == self.user_id]
        preferred_genres = self.user_preferred_genres.groupby('userId')['genre'].apply(list).reset_index()
        if user.shape[0] == 0:
            return None
        username = user.iloc[0]['username']
        password = user.iloc[0]['username']
        preferred_genres = preferred_genres.iloc[0]['genre']
        print(preferred_genres)
        return {'username': username,
                'password': password,
                'preferred_genres': preferred_genres}

    def set_user_profile(self):
        self.user_search_words = self.search_words[self.search_words['userId'] == self.user_id]
        self.user_search_genres = self.search_genres[self.search_genres['userId'] == self.user_id]
        self.user_search_years = self.search_years[self.search_years['userId'] == self.user_id]
        self.user_search_ratings = self.search_ratings[self.search_ratings['userId'] == self.user_id]
        self.user_preferred_genres = self.preferred_genres[self.preferred_genres['userId'] == self.user_id]
        self.user_movie_clicks = self.movie_clicks[self.movie_clicks['userId'] == self.user_id]

    def create_profile(self, username, password, genres):
        self.last_id += 1

        self.users.loc[self.num_users] = [self.last_id, username, password]
        self.num_users += 1

        with open('data/users.csv', 'w') as f:
            self.users.to_csv(f, index=False, header=True)

        for genre in genres:
            self.preferred_genres.loc[self.preferred_genres.shape[0]] = [self.last_id, genre]

        with open('data/preferred_genres.csv', 'w') as f:
            self.preferred_genres.to_csv(f, index=False, header=True)

        self.user_id = self.last_id

        self.set_user_profile()

        return True

    def update_preferred_genres(self, genres):
        self.user_preferred_genres['has_genre'] = [False for i in range(self.user_preferred_genres['userId'].shape[0])]

        for genre in genres:
            if genre in self.user_preferred_genres:
                self.user_preferred_genres.loc[self.user_preferred_genres['genre'] == genre, 'has_genre'] = True
            else:
                self.user_preferred_genres.loc[self.user_preferred_genres['userId'].shape[0]] = [self.user_id, genre, True]

        self.user_preferred_genres = self.user_preferred_genres[self.user_preferred_genres['has_genre']].drop(['has_genre'], axis=1)

        self.preferred_genres = self.preferred_genres[self.preferred_genres['userId'] != self.user_id]

        self.preferred_genres = self.preferred_genres.append(self.user_preferred_genres)

        with open('data/preferred_genres.csv', 'w') as f:
            self.preferred_genres.to_csv(f, index=False, header=True)

        return True

    def search_movies(self, search_term, page=1):
        start = 10 * (page - 1)
        end = 10 * page

        if page == 1:
            if search_term is not "":
                word_tokens = nltk.word_tokenize(search_term)
                # remove stop words from the search term (based on nltk library)
                terms = [w for w in word_tokens if not w in self.stop_words]
                for t in terms:
                    idx = self.user_search_words.index[(self.user_search_words['word'] == t)]
                    if idx.empty:
                        self.user_search_words.loc[self.user_search_words.shape[0]] = [self.user_id, t, 1]
                    else:
                        self.user_search_words.loc[idx, 'count'] += 1

                self.search_words = (pd.concat([self.search_words, self.user_search_words]).
                                     drop_duplicates(['userId', 'word'], keep='last'))

                with open('data/search_words.csv', 'w') as f:
                    self.search_words.to_csv(f, index=False, header=True)

                search_term = " ".join(terms)

            self.movies_list = self.r_engine.get_movies(term=search_term)

            if search_term is "":
                return self.movies_list[min(self.movies_list.shape[0], start):min(self.movies_list.shape[0], end)]

            first_movie = self.movies_list.loc[0]

            # update searched genres
            for genre in first_movie.genres.split('|'):
                idx = self.user_search_genres.index[(self.user_search_genres['genre'] == genre)]
                if idx.empty:
                    self.user_search_genres.loc[self.user_search_genres.shape[0]] = [self.user_id, genre, 1]
                else:
                    self.user_search_genres.loc[idx, 'count'] += 1

            self.search_genres = (pd.concat([self.search_genres, self.user_search_genres]).
                                  drop_duplicates(['userId', 'genre'],keep='last'))

            with open('data/search_genres.csv', 'w') as f:
                self.search_genres.to_csv(f, index=False, header=True)

        # todo add update for search_years and search_ratings
        # todo add user profile information to the result (True and False values)

        return self.movies_list[min(self.movies_list.shape[0], start):min(self.movies_list.shape[0],end)]

    def get_recommendations(self, page=1):
        start = 5 * (page - 1)
        end = 5 * page
        if page == 1:
            self.user_ratings, self.recommendations = self.r_engine.recommendation_ratings_matrix_factorization(self.user_id)
            if self.recommendations is None: return self.empty, self.empty
        return self.user_ratings, self.recommendations[min(self.recommendations.shape[0], start):min(self.recommendations.shape[0], end)]

    def rate_movie(self, movie_id, rating):
        self.r_engine.update_ratings(self.user_id, movie_id, rating)
        self.user_ratings = self.get_rated_movies()
        return True

    def get_genres(self):
        return self.r_engine.get_movies_genres()

    def update_user_data(self, username, password):
        self.users.loc[self.users['userId'] == self.user_id, 'username'] = username
        self.users.loc[self.users['userId'] == self.user_id, 'password'] = password
        with open('data/users.csv', 'w') as f:
            self.users.to_csv(f, index=False, header=True)
        return True

    def get_rated_movies(self):
        return self.r_engine.get_user_ratings(self.user_id)

    def get_movie_rating(self, movie_id):
        self.user_ratings = self.r_engine.get_user_ratings(self.user_id)
        return self.user_ratings[self.user_ratings['movieId'] == movie_id]

    def get_movie_reviews(self, movie_id, page=1):
        start = 10 * (page - 1)
        end = 10 * page
        if page == 1:
            self.reviews = self.r_engine.get_movie_tags(movie_id)
        return self.reviews[min(self.reviews.shape[0], start):min(self.reviews.shape[0],end)]

    def get_movie(self, movie_id=-1):
        if movie_id < 0:
            movie_id = self.last_movie_clicked
        return self.r_engine.get_movie(movie_id)

    def set_last_clicked_movie(self, id):
        self.last_movie_clicked = id
        return True

    def get_extra_recommendations(self, page=1):
        if self.last_movie_clicked is None:
            return self.empty
        start = 5 * (page - 1)
        end = 5 * page
        if page == 1:
            self.extra_recommendation =  self.r_engine.recommendation_ratings_correlation(self.last_movie_clicked)
        return self.extra_recommendation[min(self.extra_recommendation.shape[0], start):min(self.extra_recommendation.shape[0],end)]
