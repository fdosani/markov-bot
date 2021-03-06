from mbot import logger
log = logger.getLogger(__name__)

import sqlite3

DB_OBJECT = "db/mbot.db"

def create_table():
    """
    Function to create the inital setup of the sqlite db.
    If the DB does not exist it will create it and secondly run the ``CREATE``
    statement to make the table
    """
    conn = sqlite3.connect(DB_OBJECT)

    with conn:
        cur = conn.cursor()

        create_sql = ("CREATE TABLE tweets(user_id INT, "
                      "screen_name TEXT, tweet_id INT, "
                      "created_at TEXT, tweet TEXT)")
        cur.execute(create_sql)


def insert_tweets(records):
    """
    Function to insert list (sequence of records) of records into database

    Parameters
    ----------
    records : sequence
        A sequence object (list, tuple, etc.) which will insert records into
        the tweet table. Please see the following:
        https://docs.python.org/2/library/sqlite3.html#sqlite3.Cursor.executemany
    """
    conn = sqlite3.connect(DB_OBJECT)

    with conn:
        cur = conn.cursor()
        insert_sql = "INSERT INTO tweets VALUES (?,?,?,?,?)"
        cur.executemany(insert_sql, records)



def select_tweets(screen_name):
    """
    Function to select tweets for a paticlar user in the database

    Parameters
    ----------
    screen_name : str
        The screen_name of the twitter user in the SQLite DB you wish you query.

    Returns
    -------
    str
        A string of the all the tweets for that user with a newline ``\n``
        after each tweet.
    """
    tweet_str = ""
    conn = sqlite3.connect(DB_OBJECT)

    with conn:
        cur = conn.cursor()

        create_sql = "SELECT tweet from tweets where screen_name = ?"
        cur.execute(create_sql, (screen_name,))

        rows = cur.fetchall()
        for row in rows:
            tweet_str = tweet_str + row[0] + "\n"

    return tweet_str




def select_max_tweet_id(screen_name):
    """
    Function to select the max tweet id for a paticlar user in the database
    If the User does not exist then ``None`` is returned otherwise an ``int``
    is.

    Parameters
    ----------
    screen_name : str
        The screen_name of the twitter user in the SQLite DB you wish you query.

    Returns
    -------
    int
        The maximum tweet id of the user
    """
    conn = sqlite3.connect(DB_OBJECT)

    with conn:
        cur = conn.cursor()
        create_sql = "SELECT MAX(tweet_id) from tweets where screen_name = ?"
        cur.execute(create_sql, (screen_name,))
        id = cur.fetchone()

    return id[0]
