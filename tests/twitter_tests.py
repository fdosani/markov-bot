import unittest
from mbot import Twitter



class TestTwitter(unittest.TestCase):

    def test_twitter_init(self):
        twitter_test = Twitter(credentials_file="tests/data/config_test.ini")
        self.assertEquals(twitter_test.consumer_key, "SOME_CONSUMER_KEY")
        self.assertEquals(twitter_test.consumer_secret, "SOME_CONSUMER_SECRET")
        self.assertEquals(twitter_test.access_token, "SOME_CONSUMER_KEY")
        self.assertEquals(twitter_test.access_secret, "SOME_ACCESS_SECRET")

    def test_twitter_init(self):
        self.assertRaises(KeyError , Twitter, "tests/data/config_test.fake")


if __name__ == '__main__':
    unittest.main()
