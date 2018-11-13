import connexion
import six

from swagger_server.models.error import Error
from swagger_server.models.movie import Movie
from swagger_server import util


def movies_get(genre=None):
    """Movies

    The Movies endpoint returns information about the movies stored in the system and will be used for
    recommending other movies to a user.

    :param genre: Movie genre.
    :type genre: string

    :rtype: List[Movie]
    """
    return 'do some magic!'

