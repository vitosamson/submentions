import sqlite3
import sys
import os

db_path = os.environ['DB_PATH'] if 'DB_PATH' in os.environ else 'mentions.db'

class DB():
  def __init__(self):
    try:
      self.db = sqlite3.connect(db_path)
      self.db.execute('''
      CREATE TABLE IF NOT EXISTS mentions (
        id INTEGER PRIMARY KEY,
        mention_type TEXT,
        subreddit TEXT,
        author TEXT,
        body TEXT,
        permalink TEXT
      )
      ''')
      print('connected to sqlite db at', db_path)
    except (sqlite3.OperationalError) as err:
      print('error connecting to db')
      print(str(err))
      sys.exit(1)

  def save_mention(self, mention_type, subreddit, author, body, permalink, created_utc):
    print('saving mention: mention_type={} subreddit={} author={} permalink={} created_utc={}'.format(mention_type, subreddit, author, permalink, created_utc))

    try:
      self.db.execute('''
        INSERT INTO mentions
        (mention_type, subreddit, author, body, permalink, created_utc)
        VALUES
        (?, ?, ?, ?, ?, ?)
      ''', (mention_type, subreddit, author, body, permalink, created_utc))
      self.db.commit()

      print('saved', subreddit, permalink, flush=True)

    except (sqlite3.OperationalError) as err:
      print('error saving mention')
      print(str(err))
