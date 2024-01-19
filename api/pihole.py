# Copyright 2024 EvickaStudio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional, Union
from urllib.parse import urlparse

import requests


class API:
    """
    A wrapper class for interacting with the Pi-hole API.

    This class provides methods to make API calls to the Pi-hole admin interface
    and perform actions such as disabling the ad blocker.

    Attributes:
        api_url (str): The URL of the Pi-hole API.
        api_key (str): The API key for authentication.

    Methods:
        make_api_call: Makes an API call to the Pi-hole admin interface.
        disable_adblocker: Disables the Pi-hole ad blocker for a specified amount of time.
    """

    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def make_api_call(
        self,
        endpoint: str,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
    ) -> requests.Response:
        """
        Makes an API call to the Pi-hole admin interface.

        Args:
            endpoint (str): The API endpoint to call.
            params (Optional[dict]): The parameters to include in the API call.
            headers (Optional[dict]): The headers to include in the API call.

        Returns:
            requests.Response: The response object from the API call.
        """
        url = f"{self.api_url}{endpoint}"
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            try:
                response.raise_for_status()
                return response.json()
            except requests.exceptions.JSONDecodeError:
                raise ValueError("Invalid JSON response.")
        else:
            raise requests.exceptions.HTTPError(
                f"API call failed with status code {response.status_code}."
            )

    def disable_adblocker(self, disable_time: Union[int, float]) -> bool:
        """
        Disable the Pi-hole ad blocker for a specified amount of time.

        This makes an API call to the Pi-hole admin interface to disable ad blocking
        for the given number of seconds. It returns True if the call succeeded,
        False otherwise.

        Args:
            disable_time (Union[int, float]): Number of seconds to disable ad blocking.

        Returns:
            bool: True if the disable request succeeded, False otherwise.
        """
        params = {
            "disable": disable_time,
            "auth": self.api_key,
        }
        try:
            self.make_api_call("/admin/api.php", params)
            return True
        except requests.exceptions.HTTPError:
            return False

    @staticmethod
    def validate_api_url(api_url: str) -> bool:
        """
        Validates the Pi-hole API URL.

        Args:
            api_url (str): The URL of the Pi-hole API.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        parsed_url = urlparse(api_url)
        return all([parsed_url.scheme, parsed_url.netloc])

    @staticmethod
    def validate_api_key(api_key: str) -> bool:
        """
        Validates the Pi-hole API key.

        Args:
            api_key (str): The API key for authentication.

        Returns:
            bool: True if the key is valid, False otherwise.
        """
        return len(api_key) > 0
