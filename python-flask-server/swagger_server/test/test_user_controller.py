# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.activities import Activities  # noqa: E501
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.profile import Profile  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_history_get(self):
        """Test case for history_get

        User Activity
        """
        query_string = [('offset', 56),
                        ('limit', 56)]
        response = self.client.open(
            '/v1/history',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_me_get(self):
        """Test case for me_get

        User Profile
        """
        response = self.client.open(
            '/v1/me',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
