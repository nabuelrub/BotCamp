#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys
import io
from datetime import *
import re


#output_file and listen_time name are argument 


#Variables that contains the user credentials to access Twitter API # unmdscs4 Account
#==================Add Twitter Authentication key==================
access_token = "792415190805516289-RPsyCM24K4j6rgyw7TxhZJ5AJ9089Me"
access_token_secret = "mWz3iShCO7X0wNTCGOe9VZXTuQqyKF9qAs6rc1r2lsgGO"
consumer_key = "GefZR3duK7gNGKcycNAwKYhYS"
consumer_secret = "6PVYp7dfKJ1nuc4daZFjsJhsvfI13s4UwVrxXDD964oVtuS3PS"


API_file_name = sys.argv[1]
API_file = open (API_file_name+'/trends.txt','w')

if __name__ == '__main__':
	
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	api = tweepy.API(auth)
	cur_time = datetime.now()
	trends1 = api.trends_place(23424977)
	#trend by place. You can find the place id(called woeid) here: http://woeid.rosselliot.co.nz/
	#trends1 = api.trends_place(23424977)
	data = trends1[0] 
	# grab the trends
	trends = data['trends']
	# grab the name from each trend
	API_filter = [trend['name'] for trend in trends]
	volumes = [trend['tweet_volume'] for trend in trends]
	print API_filter
	#API_file.write(str(cur_time) + '\n')
	for ii in range(len(API_filter)):
		API_file.write(API_filter[ii].encode('utf-8') + '\n')
	#API_file.write(API_filter[-1].encode('utf-8') + ',' + str(volumes[-1]) + '\n')
	API_file.close()	

