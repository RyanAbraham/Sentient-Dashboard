# to install tweepy -> pip install tweepy

import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import indicoio

#Use your keys
# consumer_key = '...'
# consumer_secret = '...'
# access_token = '...'
# access_secret = '...'
# indicoio.config.api_key = '...'
# search_term = "happiness"

def get_tweets():
	index = 0
	search_results = {}

	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	# searches count num of tweets containing string q
	search_results = api.search(q=search_term, count=30)
	# public_tweets = api.home_timeline()

	print("Showing tweets with keyphrase...")

	# uses indico's emotion analyzer to return any "happy" tweets as text
	for tweet in search_results:
            if (indicoio.emotion(tweet.text).get('joy') > 0.55):
                index += 1
                search_results[index] = tweet.text

	return json.dumps(search_results)
