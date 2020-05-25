# coding: utf-8

# Copyright 2019, 2020 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from abc import ABC, abstractmethod
from typing import Optional

import jwt

from .token_manager import TokenManager


# pylint: disable=too-many-instance-attributes


class JWTTokenManager(TokenManager, ABC):
    """An abstract class to contain functionality for parsing, storing, and requesting JWT tokens.

    get_token will retrieve a new token from the url in case the that there is no existing token,
    or the previous token has expired. Child classes will implement request_token, which will do
    the actual acquisition of a new token.

    Args:
        url: The url to request tokens from.

    Keyword Args:
        disable_ssl_verification: A flag that indicates whether verification of
            the server's SSL certificate should be disabled or not. Defaults to False.
        token_name: The key that maps to the token in the dictionary returned from request_token. Defaults to None.

    Attributes:
        url (str): The url to request tokens from.
        disable_ssl_verification (bool): A flag that indicates whether verification of
        the server's SSL certificate should be disabled or not.
        token_name (str): The key used of the token in the dict returned from request_token.
        token_info (dict): The most token_response from request_token.
    """

    def __init__(self, url: str, *, disable_ssl_verification: bool = False, token_name: Optional[str] = None):
        super().__init__(url, disable_ssl_verification=disable_ssl_verification)
        self.token_name = token_name
        self.token_info = {}

    def _save_token_info(self, token_response: dict) -> None:
        """
        Decode the access token and save the response from the JWT service to the object's state
        Refresh time is set to approximately 80% of the token's TTL to ensure that
        the token refresh completes before the current token expires.
        Parameters
        ----------
        token_response : dict
            Response from token service
        """
        self.token_info = token_response
        access_token = token_response.get(self.token_name)

        # The time of expiration is found by decoding the JWT access token
        decoded_response = jwt.decode(access_token, verify=False)
        # exp is the time of expire and iat is the time of token retrieval
        exp = decoded_response.get('exp')
        iat = decoded_response.get('iat')

        buffer = (exp - iat)

        self._set_expire_and_refresh_time(exp, buffer)

    def extract_token_from_stored_response(self):
        """Get the token from the stored response

        Returns:
            str: The stored access token
        """
        return self.token_info.get(self.token_name)

    def _request(self,
                 method,
                 url,
                 *,
                 headers=None,
                 params=None,
                 data=None,
                 auth_tuple=None,
                 **kwargs) -> dict:
        return self._request_raw(method, url, headers=headers, params=params, data=data,
                                 auth_tuple=auth_tuple, **kwargs).json()

    @abstractmethod
    def request_token(self) -> None:  # pragma: no cover
        """Should be overridden by child classes.
        """
        pass
