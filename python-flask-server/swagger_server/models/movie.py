# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime

from typing import List, Dict

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Movie(Model):

    def __init__(self, movie_id: int=None, title: str=None, genres: str=None):
        """Movie - a model defined in Swagger

        :param movie_id: The movie_id of this Movie.
        :type movie_id: str
        :param title: The title of this Movie.
        :type title: str
        :param genres: The genres of this Movie.
        :type genres: str
        """
        self.swagger_types = {
            'movie_id': int,
            'title': str,
            'genres': str,
        }

        self.attribute_map = {
            'movie_id': 'movie_id',
            'title': 'title',
            'genres': 'genres',
        }

        self._movie_id = movie_id
        self._title = title
        self._genres = genres

    @classmethod
    def from_dict(cls, dikt) -> 'Movie':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Movie of this Movie.
        :rtype: Movie
        """
        return util.deserialize_model(dikt, cls)

    @property
    def movie_id(self) -> int:
        """Gets the movie_id of this Movie.

        Unique identifier representing a specific movie.

        :return: The movie_id of this Movie.
        :rtype: int
        """
        return self._movie_id

    @movie_id.setter
    def movie_id(self, movie_id: str):
        """Sets the movie_id of this Movie.

        Unique identifier representing a specific movie.

        :param movie_id: The movie_id of this Movie.
        :type movie_id: str
        """

        self._movie_id = movie_id

    @property
    def title(self) -> str:
        """Gets the title of this Movie.

        :return: The title of this Movie.
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets the title of this Movie.

        :param title: The title of this Movie.
        :type title: str
        """

        self._title = title

    @property
    def genres(self) -> str:
        """Gets the genres of this Movie.

        :return: The genres of this Movie.
        :rtype: str
        """
        return self._genres

    @genres.setter
    def genres(self, genres: str):
        """Sets the genres of this Movie.

        :param genres: The genres of this Movie.
        :type genres: str
        """

        self._genres = genres
