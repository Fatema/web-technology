from flask import json
import nltk
from nltk.corpus import stopwords

from recommendation_engine import RecommendationEngine

class Service:

    def __init__(self):
        self.r_engine = RecommendationEngine()

        # all this information shouldn't be part of the api but for the sake of this assignment it is here
        with open('data/user_profile.json') as f:
            self.users = json.load(f)["profiles"]

        self.num_users = len(self.users)
        self.last_id = self.r_engine.get_latest_user_id()

        self.user_profile = None

        self.stop_words = set(stopwords.words('english'))

    def has_profile(self, username):
        for user in self.users:
            if user["user_name"] == username:
                self.user_profile = user
                return True
        return False

    def add_new_profile(self, username, genres):
        self.last_id += 1
        new_profile = {"user_id": self.last_id,
                       "user_name": username,
                       "preferred_genres" : genres,
                       "search_words" : [],
                       "search_years" : [],
                       "search_genres" : [],
                       "search_ratings" : [],
                       "movie_clicks" : [],
                       "movie_ratings" : []
                      }
        self.users[self.num_users] = new_profile
        self.num_users += 1

        with open('data/user_profile.json', 'w') as f:
            json.dump({"profiles": self.users}, f)

        self.user_profile = new_profile

        return True

    def find_movies(self, search_term):
        word_tokens = nltk.word_tokenize(search_term)
        terms = [w for w in word_tokens if not w in self.stop_words]
        for t in terms:
            is_sw = False
            for w in self.user_profile["search_words"]:
                if t is w["word"]:
                    w.update((t, w["count"] + 1))
                    is_sw = True
                    break
            if not is_sw:
                self.user_profile["search_words"].append({"word": t, "count": 1})

        movies_list = self.r_engine.get_movies(self.user_profile["user_id"])

        # todo add call to r_engine to get the movie based on the search_term
        # make use of the user_profile as well if possible

        # user the user profile to determine the order of the movies outputted

    def get_movies(self):
        if self.user_profile is None or \
                len(self.user_profile["movie_ratings"]) == 0:
            return {"all_movies" : self.r_engine.get_movies()}

    def rate_movie(self, movie_id, rating):
        self.r_engine.update_ratings(self.user_profile["user_id"], movie_id, rating)
        return True
