import requests

class Slack():
  def __init__(self, webhook_url):
    if not webhook_url:
      print('missing slack webhook_url')
      exit(1)

    self.webhook_url = webhook_url

  def post_mention(self, mention_type, title, subreddit, author, body, permalink):
    payload = {
      'attachments': [{
        'title': title,
        'text': body,
        'fallback': 'https://www.reddit.com' + permalink,
        'color': 'good' if mention_type == 'comments' else 'warning',
        'fields': [{
          'title': 'Subreddit',
          'value': '<https://www.reddit.com/r/{}|/r/{}>'.format(subreddit, subreddit),
          'short': True
        }, {
          'title': 'Author',
          'value': '<https://www.reddit.com/user/{}|/u/{}>'.format(author, author),
          'short': True
        }, {
          'title': 'Link',
          'value': 'https://www.reddit.com{}?context=3'.format(permalink)
        }]
      }]
    }

    try:
      requests.post(self.webhook_url, json=payload)
    except requests.exceptions.RequestException as err:
      print('could not post to slack: ' + str(err))
