import unittest
import mock

from mbot import Twitter
from mbot.twitter import tweepy



class TestTwitter(unittest.TestCase):

    def test_twitter_init(self):
        twitter_test = Twitter(credentials_file="tests/data/config_test.ini")

        self.assertEquals(twitter_test.consumer_key, "SOME_CONSUMER_KEY")
        self.assertEquals(twitter_test.consumer_secret, "SOME_CONSUMER_SECRET")
        self.assertEquals(twitter_test.access_token, "SOME_ACCESS_TOKEN")
        self.assertEquals(twitter_test.access_secret, "SOME_ACCESS_SECRET")



    def test_twitter_init_exception(self):
        self.assertRaises(KeyError , Twitter, "tests/data/config_test.fake")



    def test_twitter_authenticate(self):
        twitter_test = Twitter(credentials_file="tests/data/config_test.ini")
        api_test = twitter_test._authenticate()
        auth_test = api_test.auth

        self.assertEquals(auth_test.consumer_key, b"SOME_CONSUMER_KEY")
        self.assertEquals(auth_test.consumer_secret, b"SOME_CONSUMER_SECRET")
        self.assertEquals(auth_test.access_token, "SOME_ACCESS_TOKEN")
        self.assertEquals(auth_test.access_token_secret, "SOME_ACCESS_SECRET")



    @mock.patch.object(tweepy, "Cursor")
    @mock.patch.object(tweepy.API, "user_timeline")
    def test_twitter_get_tweets(self, mock_timeline, mock_cursor):
        twitter_test = Twitter(credentials_file="tests/data/config_test.ini")


        #normal usage
        mocked_tweets = twitter_test.get_tweets("twitter_user")
        mock_cursor.assert_called_with(mock_timeline,
                                       screen_name="twitter_user",
                                       include_rts=False)

        #normal usage
        mocked_tweets = twitter_test.get_tweets("twitter_user",
                                                include_rts=True)
        mock_cursor.assert_called_with(mock_timeline,
                                       screen_name="twitter_user",
                                       include_rts=True)

        #exception
        mock_cursor.side_effect = tweepy.TweepError('Mock Exception')
        self.assertRaises(tweepy.TweepError,
                          twitter_test.get_tweets,
                          "twitter_user")





    @mock.patch.object(tweepy, "Cursor")
    @mock.patch.object(tweepy.API, "user_timeline")
    def test_twitter_get_tweets_loop(self, mock_timeline, mock_cursor):

        mock_user = tweepy.models.User()
        mock_user.id = 1234
        mock_user.screen_name = "twitter_user"

        status_1 = tweepy.models.Status()
        status_1.text = "A mocked up tweet"
        status_1.created_at = "2016-01-01"
        status_1.user = mock_user

        status_2 = tweepy.models.Status()
        status_2.text = "A mocked up tweet number two"
        status_2.created_at = "2016-01-02"
        status_2.user = mock_user

        mock_cursor.return_value.items.return_value = [status_1, status_2]

        twitter_test = Twitter(credentials_file="tests/data/config_test.ini")
        mocked_tweets = twitter_test.get_tweets("twitter_user")

        self.assertEquals(mocked_tweets, [[mock_user.id, mock_user.screen_name,
                                           status_1.created_at, status_1.text],
                                          [mock_user.id, mock_user.screen_name,
                                           status_2.created_at, status_2.text]])

if __name__ == '__main__':
    unittest.main()
