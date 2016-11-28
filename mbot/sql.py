from mbot import logger
log = logger.getLogger(__name__)

import sqlite3

DB_OBJECT = "db/mbot.db"

def init_setup():
    """
    Function to create the inital setup of the sqlite db
    """
    conn = sqlite3.connect(DB_OBJECT)
