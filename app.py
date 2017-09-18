import json
from time import sleep
import os
import traceback
import praw #pylint: disable=import-error
import prawcore #pylint: disable=import-error
from db import DB

data = {}

try:
  with open('./credentials.json') as data_file:
    data = json.load(data_file)
except FileNotFoundError:
  print('missing credentials')
  exit(1)

reddit_app_key = data["script"]["client_id"]
reddit_app_secret = data["script"]["client_secret"]
reddit_user_name = data["user"]["username"]
reddit_user_password = data["user"]["password"]
reddit_user_agent = "mod utils v0.1"

reddit = praw.Reddit(user_agent=reddit_user_agent,
                     client_id=reddit_app_key,
                     client_secret=reddit_app_secret,
                     username=reddit_user_name,
                     password=reddit_user_password)

mention_type = 'submissions' if 'TYPE' in os.environ and os.environ['TYPE'] == 'submissions' else 'comments'
sub_name = 'neutralpolitics'

db = DB()

print('user:', reddit_user_name)
print('key:', reddit_app_key)
print('mention type:', mention_type, flush=True)

def main():
  stream = reddit.subreddit('all').stream
  stream = stream.comments() if mention_type == 'comments' else stream.submissions()

  for item in stream:
    if mention_type == 'comments':
      if sub_name in item.body.lower() and sub_name not in item.permalink().lower():
        db.save_mention(mention_type,
                        str(item.subreddit).lower(),
                        str(item.author).lower(),
                        item.body,
                        item.permalink(),
                        int(item.created_utc))
    elif mention_type == 'submissions':
      if sub_name in item.url.lower() and sub_name not in str(item.subreddit).lower():
        db.save_mention(mention_type,
                        str(item.subreddit).lower(),
                        str(item.author).lower(),
                        item.selftext,
                        item.permalink,
                        int(item.created_utc))

while True:
  try:
    main()
  except praw.exceptions.APIException as err:
    print('rate limit hit, sleeping 100 secs')
    print(str(err), flush=True)
    sleep(100)
  except prawcore.exceptions.ServerError as err:
    print('reddit API error, sleeping 30 secs')
    print(str(err), flush=True)
    sleep(30)
  except Exception as err:
    print(str(err), flush=True)
    traceback.print_exc()
    sleep(1)
  finally:
    main()