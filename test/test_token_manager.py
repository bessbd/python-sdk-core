# coding: utf-8

# Copyright 2020 IBM All Rights Reserved.
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

# pylint: disable=missing-docstring,protected-access

import pytest

from ibm_cloud_sdk_core.token_manager import TokenManager


def test_request_token_not_implemented_error():
    with pytest.raises(NotImplementedError) as err:
        token_manager = TokenManager(None)
        token_manager.request_token()
    assert str(err.value) == 'request_token MUST be overridden by a subclass of TokenManager.'


def test_extract_exp_and_ttl_not_implemented_error():
    with pytest.raises(NotImplementedError) as err:
        token_manager = TokenManager(None)
        token_manager.extract_exp_and_ttl(None)
    assert str(err.value) == 'extract_exp_and_ttl MUST be overridden by a subclass of TokenManager.'
