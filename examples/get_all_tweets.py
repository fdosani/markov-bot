from mbot import Twitter, sql

twitter_user = "realDonaldTrump"
#grab all of donalds tweets
trump = Twitter()
trumps_tweets = trump.get_tweets(twitter_user)
sql.insert_tweets(trumps_tweets)
