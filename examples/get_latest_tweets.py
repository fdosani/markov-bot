from mbot import Twitter, sql

twitter_user = "realDonaldTrump"

#grab new (since) donald tweets
trump = Twitter()
since_id = sql.select_max_tweet_id(twitter_user)
trumps_tweets = trump.get_tweets(twitter_user, since_id)
sql.insert_records(trumps_tweets)
