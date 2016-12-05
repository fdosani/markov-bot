try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from mbot import logger
log = logger.getLogger(__name__)

import tweepy


class Twitter:
    """Twitter class which is meant to interact with the Twitter API. It will
    manage reading the API keys and secrets from a ``ini`` file, and also get
    all tweets (statuses) for a user or since a paticular status id

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


    def get_tweets(self, screen_name, since_id=None, include_rts=False):
        """Get the tweets from a paticular users timeline to help build a
        corpus. Is not date sensitve and will get ALL tweets it can.

        Note
        ----
        Twitter only allows 3200 tweets to be returned so if this is a new
        users tweets which you are grabbing, please keep that in mind.


        Parameters
        ----------
        screen_name : str
            the twitter handle which you want to get tweets for

        since_id : int, optional
            the status(tweet) id to get rest of timeline since. This will
            help in getting most recent tweets rather than getting them all
            again. If ``None`` then get all tweets possible.

        include_rts : bool, optional
            True or False on if you would like to include retweets from
            timeline.

        Returns
        -------
        list
            list of lists containing:
                * user id
                * user screen name
                * tweet id
                * tweet created_at date
                * tweet text
        """
        tweets = []
        try:
            if since_id is None:
                statuses = tweepy.Cursor(self.api.user_timeline,
                                         screen_name=screen_name,
                                         include_rts=include_rts).items()
            else:
                statuses = tweepy.Cursor(self.api.user_timeline,
                                         screen_name=screen_name,
                                         since_id=since_id,
                                         include_rts=include_rts).items()

            log.info('getting tweets for user: {0}'.format(screen_name))
            for status in statuses:
                tweets.append([status.user.id,
                               status.user.screen_name,
                               status.id,
                               status.created_at,
                               status.text])

            return tweets
        except tweepy.TweepError as e:
            log.error('twitter api error: {0}'.format(e))
            raise
