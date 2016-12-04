import unittest
import mock

from mbot import sql




class TestSQL(unittest.TestCase):

    @mock.patch.object(sql.sqlite3, "connect")
    def test_sql_create_table(self, mock_sql):

        create_sql = ("CREATE TABLE tweets(user_id INT, screen_name TEXT, "
                      "tweet_id INT, created_at TEXT, tweet TEXT)")

        sql.create_table()
        mock_sql.assert_called_with(sql.DB_OBJECT)
        mock_sql.return_value.cursor.assert_called_with()
        mock_sql.return_value.cursor.return_value.\
                              execute.assert_called_with(create_sql)



    @mock.patch.object(sql.sqlite3, "connect")
    def test_sql_insert_records(self, mock_sql):

        insert_sql = "INSERT INTO tweets VALUES (?,?,?,?,?)"
        insert_data = [[1,2,3,4,5],[6,7,8,9,10]]

        sql.insert_records(insert_data)
        mock_sql.assert_called_with(sql.DB_OBJECT)
        mock_sql.return_value.cursor.assert_called_with()

        mock_sql.return_value.cursor.return_value.\
                              executemany.assert_called_with(insert_sql,
                                                             insert_data)



    @mock.patch.object(sql.sqlite3, "connect")
    def test_sql_select_tweets(self, mock_sql):

        screen_name = "twitter_user"
        create_sql = ("SELECT tweet from tweets "
                      "where screen_name = ?")
        return_data = [["tweet1",], ["tweet2",]]
        mock_sql.return_value.cursor.return_value.\
                              fetchall.return_value = return_data


        actual = sql.select_tweets(screen_name)

        mock_sql.assert_called_with(sql.DB_OBJECT)
        mock_sql.return_value.cursor.assert_called_with()

        mock_sql.return_value.cursor.return_value.\
                              execute.assert_called_with(create_sql,
                                                         (screen_name,))

        mock_sql.return_value.cursor.return_value.\
                              fetchall.assert_called_with()

        self.assertEquals(actual, "tweet1\ntweet2\n")


    @mock.patch.object(sql.sqlite3, "connect")
    def test_sql_select_max_tweet_id(self, mock_sql):

        screen_name = "twitter_user"
        create_sql = "SELECT MAX(tweet_id) from tweets where screen_name = ?"
        return_data = (1234,)
        mock_sql.return_value.cursor.return_value.\
                              fetchone.return_value = return_data


        actual = sql.select_max_tweet_id(screen_name)

        mock_sql.assert_called_with(sql.DB_OBJECT)
        mock_sql.return_value.cursor.assert_called_with()

        mock_sql.return_value.cursor.return_value.\
                              execute.assert_called_with(create_sql,
                                                         (screen_name,))

        mock_sql.return_value.cursor.return_value.\
                              fetchone.assert_called_with()

        self.assertEquals(actual, 1234)



if __name__ == '__main__':
    unittest.main()
