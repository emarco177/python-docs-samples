# Copyright 2021, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import google.auth
import pytest
import requests

import vm_identity

AUDIENCE = 'http://www.testing.com'


def test_vm_identity():
    try:
        # Check if we're running in a GCP VM:
        _ = requests.get('http://metadata.google.internal/computeMetadata/v1/',
                         headers={'Metadata-Flavor': 'Google'})
    except requests.exceptions.ConnectionError:
        # Guess we're not running in a GCP VM, we need to skip this test
        pytest.skip("Test can only be run inside GCE VM.")

    token = vm_identity.acquire_token(AUDIENCE)
    assert isinstance(token, str) and token
    verification = vm_identity.verity_token(token, AUDIENCE)
    assert isinstance(verification, dict) and verification
    assert verification['aud'] == AUDIENCE
    assert verification['email_verified']
    assert verification['iss'] == 'https://accounts.google.com'
    assert verification['google']['compute_engine']['project_name'] == google.auth.default()[1]
