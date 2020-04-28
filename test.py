import hibpwned
import unittest
pwned = hibpwned.Pwned('test@example.com', 'wrapper_test', 'No Key')


class TestApiCalls(unittest.TestCase):
    """pass"""


    def test_searchPassword(self):

        #
        week = pwned.searchPassword('password')
        self.assertTrue(week.isdigit())


    def test_singleBreach(self):

        #
        name = pwned.singleBreach('adobe')['Name']
        self.assertEqual(name, 'Adobe')


    def test_allBreaches(self):

        #
        length = len(pwned.allBreaches())
        self.assertTrue(length > 439)


    def test_searchHashes(self):

        # make sure response is not integer 400
        password_hash = pwned.searchHashes('5baa6')
        self.assertFalse(password_hash.isdigit())


    def test_dataClasses(self):

        #
        lst = type(pwned.dataClasses())
        self.assertTrue(lst, 'list')

if __name__ == '__main__':
    unittest.main()

