try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from mbot import logger
log = logger.getLogger(__name__)

import tweepy


class Twitter:
    """Exceptions are documented in the same way as classes.

    The __init__ method may be documented in either the class level
    docstring, or as a docstring on the __init__ method itself.

    Either form is acceptable, but the two should not be mixed. Choose one
    convention to document the __init__ method and be consistent with it.

    Note
    ----
    Do not include the `self` parameter in the ``Parameters`` section.

    Parameters
    ----------
    credentials_file : str. optional
        String representing the location of the twitter credentials ini file.
        By default the current working directory will be inspected for a file
        called: `config.ini`

    Attributes
    ----------
    consumer_key : str
        Your Twitter user's consumer key
    consumer_secret : str
        Your Twitter user's consumer secret.
    access_token : str
        Your Twitter applications access token
    access_secret : str
        Your Twitter applications access secret
    """
    def __init__(self, credentials_file="config.ini"):
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_secret = None
        self.api = None
        try:
            (self.consumer_key, self.consumer_secret, self.access_token,
             self.access_secret) = self._read_ini(credentials_file)

            self.api = self._authenticate()
        except KeyError:
            log.error('error reading config file: {0}'.format(credentials_file))
            raise


    def _read_ini(self, file_name):
        """Read the config file using ConfigParser for the Twitter
        authentication variables.

        Parameters
        ----------
        file_name : str
            String representing the INI file which holds the Twitter OAuth
            variables (consumer_key, consumer_secret, access_token,
            access_secret)

        Returns
        -------
        tuple
            Tuple of strings with the parsed out OAuth details:
            * consumer_key
            * consumer_secret
            * access_token
            * access_secret
        """
        config = configparser.ConfigParser()
        log.info('reading config file: {0}'.format(file_name))
        config.read(file_name)
        return (config["twitter"]["consumer_key"],
                config["twitter"]["consumer_secret"],
                config["twitter"]["access_token"],
                config["twitter"]["access_secret"])


    def _authenticate(self):
        """Returns the tweepy API handler which is used to interact with the
        Twitter API with the proper OAuth input variables

        Returns
        -------
        tweepy.api.API
            tweepy Twitter API wrapper for the API as provided by Twitter
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        return tweepy.API(auth)


    def get_tweets(self, screen_name):
        """Get the tweets from a paticular users timeline to help build a corpus

        Parameters
        ----------
        screen_name : str
            the twitter handle which you want to get tweets for

        """
        tweets = []
        try:
            statuses = tweepy.Cursor(self.api.user_timeline,
                                     screen_name=screen_name,
                                     include_rts=True).items(10)

            log.info('getting tweets for user: {0}'.format(screen_name))
            for status in statuses:
                tweets.append([status.user.id,
                               status.user.screen_name,
                               status.text])

            return tweets
        except tweepy.TweepError as e:
            log.error('twitter api error: {0}'.format(e))
            raise
