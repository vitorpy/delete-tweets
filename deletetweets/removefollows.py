import io
import os
import sys
import json

import twitter
from datetime import datetime
from dateutil import parser

class TweetUnfollower(object):
    def __init__(self, twitter_api, dry_run=False):
        self.twitter_api = twitter_api
        self.dry_run = dry_run

    def destroy(self, all, tweet_id):
        try:
            user = self.twitter_api.GetUser(user_id=tweet_id)

            print("delete friend %s" % user.screen_name)
            if not self.dry_run:
                if not all:
                    self.twitter_api.DestroyFriendship(user_id=tweet_id)
                self.twitter_api.DestroyMute(user_id=tweet_id)
        except twitter.TwitterError as err:
            print("Exception: %s\n" % err.message)

def delete(all, dry_run=False):
    api = twitter.Api(consumer_key=os.environ["TWITTER_CONSUMER_KEY"],
                      consumer_secret=os.environ["TWITTER_CONSUMER_SECRET"],
                      access_token_key=os.environ["TWITTER_ACCESS_TOKEN"],
                      access_token_secret=os.environ["TWITTER_ACCESS_TOKEN_SECRET"],
                      sleep_on_rate_limit=True)
    destroyer = TweetUnfollower(api, dry_run)

    mutes = set(api.GetMutesIDs())
    friends = set(api.GetFriendIDs())

    target = mutes
    if not all:
        target = mutes.intersection(friends)

    for id in target:
        destroyer.destroy(all, id)

    sys.exit()
