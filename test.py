"""A human friendly python API wrapper for https://haveibeenpwned.com
   All data is sourced from https://haveibeenpwned.com
   Visit https://haveibeenpwned.com/API/v3 to read the Acceptable Use Policy
   for rules regarding acceptable usage of this API.

   Copyright (C) 2020  plasticuproject@pm.me

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
"""

import unittest
from unittest import mock
from typing import Optional, Union, List, Dict, Any
import requests
import hibpwned


# pylint: disable=unused-argument
def mocked_requests_get(*args: Any, **kwargs: Any) -> Any:
    """This method will be used by the mock to replace requests.get."""

    class MockResponse:  # pylint: disable=too-few-public-methods
        """Mock API responses."""

        def __init__(self, response_data: Optional[Union[List[str],
                                                         Dict[str, str]]],
                     status_code: int) -> None:
            self.response_data = response_data
            self.status_code = status_code

        def json(self) -> Optional[Union[List[str], Dict[str, str]]]:
            """Returns mocked API response data."""
            return self.response_data

    if args[0] == ("https://haveibeenpwned.com/api/v3/breachedaccount/" +
                   "test@example.com"):
        return MockResponse(["FakeSite"], 200)
    if args[0] == ("https://haveibeenpwned.com/api/v3/breachedaccount/" +
                   "test@example.com?truncateResponse=false"):
        return MockResponse({"testKey": "testValue"}, 200)
    if args[0] == ("https://haveibeenpwned.com/api/v3/pasteaccount/" +
                   "test@example.com"):
        return MockResponse({"testKey": "testValue"}, 200)
    return MockResponse(None, 404)


class TestApiCalls(unittest.TestCase):
    """Test all module API calls."""

    email: str = "test@example.com"
    app_name: str = "wrapper_test"
    key: str = "No Key"
    pwned = hibpwned.Pwned(email, app_name, key)

    def test_search_password(self) -> None:
        """Test search_password function."""

        # test that a found password returns the number of times
        # that it is found.
        weak = self.pwned.search_password("password")
        if isinstance(weak, str):
            self.assertTrue(weak.isdigit())

    def test_single_breach(self) -> None:
        """Test single_breach function."""

        # test that the Adobe information is returned when searching
        # for that single breach
        names = self.pwned.single_breach("adobe")
        if isinstance(names, list):
            name = names[0]["Name"]
        self.assertEqual(name, "Adobe")

        # test for 404 when searching for breach name not in the database
        bad_name = self.pwned.single_breach("bullshit")
        self.assertEqual(bad_name, 404)

    def test_all_breaches(self) -> None:
        """Test all_breaches function."""

        # test that calling for all breaches returns an object
        # with the length of the amount of breaches found, which
        # as of 04/28/2020 should be more than 439
        length_test = self.pwned.all_breaches()
        if isinstance(length_test, list):
            list_length = len(length_test)
        self.assertTrue(list_length > 439)

        # Test searching for vaild name returns name
        names = self.pwned.all_breaches(domain="adobe.com")
        if isinstance(names, list):
            domain_name = names[0]
        self.assertEqual(domain_name["Name"], "Adobe")

    def test_search_hashes(self) -> None:
        """Test search_hashes function."""

        # test that response for querying a hash is not a response code
        # error 400, which is recieved as an integer
        password_hash = self.pwned.search_hashes("5baa6")
        self.assertFalse(str(password_hash).isdigit())
        bad_hash = self.pwned.search_hashes("beef")
        self.assertEqual(bad_hash, 400)

    def test_data_classes(self) -> None:
        """Test data_classes function."""

        # test that querying for the database data classes returns a list
        lst = type(self.pwned.data_classes())
        self.assertTrue(lst, "list")

    def test_search_all_breaches(self) -> None:
        """Test search_all_breaches function."""

        # test breach search with no key errors
        bad_key = self.pwned.search_all_breaches()
        bad_key_name = self.pwned.search_all_breaches(domain="adobe.com")
        bad_key_trunc_unver = self.pwned.search_all_breaches(truncate=True,
                                                             unverified=True)
        self.assertEqual(bad_key, 401)
        self.assertEqual(bad_key_name, 401)
        self.assertEqual(bad_key_trunc_unver, 401)

    def test_search_pastes(self) -> None:
        """Test search_pastes function."""

        # test paste search errors with bad key
        bad_key = self.pwned.search_pastes()
        self.assertEqual(bad_key, 401)

    @mock.patch("requests.get", side_effect=mocked_requests_get)
    def test_mock_error(self, mock_get: mock.MagicMock) -> None:
        """Test a non-recognized mock endpoint will return a
        status code 404."""
        bad_url = requests.get("https://www.fart.com")
        self.assertEqual(bad_url.status_code, 404)

    @mock.patch("hibpwned.requests.get", side_effect=mocked_requests_get)
    def test_mock_search_all_breaches(self, mock_get: mock.MagicMock) -> None:
        """Test search_all_breaches against mock API, since we do not
        have a valid API-Key to test againt the live API."""
        no_trunc_data = self.pwned.search_all_breaches()
        if isinstance(no_trunc_data, list):
            self.assertEqual(no_trunc_data[0], {"testKey": "testValue"})
        trunc_data = self.pwned.search_all_breaches(truncate=True)
        if isinstance(trunc_data, list):
            self.assertEqual(trunc_data[0], "FakeSite")

    @mock.patch("hibpwned.requests.get", side_effect=mocked_requests_get)
    def test_mock_search_pastes(self, mock_get: mock.MagicMock) -> None:
        """Test search_pastes against mock API, since we do not
        have a valid API-Key to test againt the live API."""
        pastes = self.pwned.search_pastes()
        if isinstance(pastes, list):
            self.assertEqual(pastes[0], {"testKey": "testValue"})


if __name__ == "__main__":
    unittest.main()
