"""A human friendly python API wrapper for https://haveibeenpwned.com
   All data is sourced from https://haveibeenpwned.com
   Visit https://haveibeenpwned.com/API/v3 to read the Acceptable Use Policy
   for rules regarding acceptable usage of this API.

   Copyright (C) 2018  plasticuproject@pm.me

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License.
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
"""


import hibpwned
import unittest
pwned = hibpwned.Pwned('test@example.com', 'wrapper_test', 'No Key')


class TestApiCalls(unittest.TestCase):
    """Test all module api calls that do not require a HIBP-API-KEY"""


    def test_searchPassword(self):

        # test that a found password returns the number of times 
        # that it is found.
        week = pwned.searchPassword('password')
        self.assertTrue(week.isdigit())


    def test_singleBreach(self):

        # test that the Adobe information is returned when searching
        # for that single breach 
        name = pwned.singleBreach('adobe')['Name']
        self.assertEqual(name, 'Adobe')


    def test_allBreaches(self):

        # test that calling for all breaches returns an object
        # with the length of the amount of breaches found, which
        # as of 04/28/2020 should be more than 439
        length = len(pwned.allBreaches())
        self.assertTrue(length > 439)


    def test_searchHashes(self):

        # test that response for querying a hash is not a resonse code
        # error 400, which is recieved as an integer
        password_hash = pwned.searchHashes('5baa6')
        self.assertFalse(password_hash.isdigit())


    def test_dataClasses(self):

        # test that querying for the database data classes returns a list
        # object
        lst = type(pwned.dataClasses())
        self.assertTrue(lst, 'list')

if __name__ == '__main__':
    unittest.main()

