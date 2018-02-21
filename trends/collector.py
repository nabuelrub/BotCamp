#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import sys
import io
from datetime import *
from httplib import IncompleteRead
import re
import codecs
#iteration, listen_time, and round_path are arguments


#Variables that contains the user credentials to access Twitter API 
#==================Add Twitter Authentication key==================

access_token = "792415190805516289-RPsyCM24K4j6rgyw7TxhZJ5AJ9089Me"
access_token_secret = "mWz3iShCO7X0wNTCGOe9VZXTuQqyKF9qAs6rc1r2lsgGO"
consumer_key = "GefZR3duK7gNGKcycNAwKYhYS"
consumer_secret = "6PVYp7dfKJ1nuc4daZFjsJhsvfI13s4UwVrxXDD964oVtuS3PS"


itr = str(sys.argv[1])
listen_time = int(sys.argv[2]) #insecond
round_path = sys.argv[3]

output_file_name = str(round_path)+'/'+str(itr) + '.txt'
output_file = open(output_file_name,'w')

API_file_name = str(round_path)+'/filter.txt'
API_file = io.open (API_file_name,'at',encoding='utf-8')

new_tweet_f =  str(round_path)+'/'+'new_tweet'
in_file_f  =  str(round_path)+'/'+'in_file'

#Sample of API filters:
keywords = codecs.open(round_path+'/trends.txt','r',encoding="utf-8")
API_filter = []
for line in keywords:
	#print line
	line = line.rsplit('\n')[0]
	print line
	API_filter.append(line)
#API_filter = ['instagram','swarmapp','youtube']
print "keywords :", API_filter
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
	
	def __init__(self, api=None):
		super(StdOutListener, self).__init__()
		self.prev_time = datetime.now()
		self.next_time = datetime.now()
	
	'''def on_status(self,status):
		
		#test_1 = status.json 		
		print str(status.created_at) + ' ' + str(status.user.screen_name)+ ' ' +  str(status.user.id)
		return True'''
	def on_data(self, data):
		self.next_time = datetime.now()
		if (self.next_time - self.prev_time).total_seconds() < listen_time: 
			try:
				output_file.write(str(data))
				#--------------OR
				#x = json.loads(data)
				#output_file.write(str(x['created_at']) + "," + str(x['user']['screen_name']) + "," + str(x['user']['id']) + "\n")
				return True
			except:
				return True
		else:
			return False
	def on_error(self, status):
		print status


if __name__ == '__main__':
	#This handles Twitter authetification and the connection to Twitter Streaming API
	l = StdOutListener()
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	

	api = tweepy.API(auth)
	#try catch was added to solve incomplete read problem
	try:
		stream = Stream(auth, l)
		stream.filter(track=API_filter)		
	except IncompleteRead:
		pass
		
	new_tweet = open(new_tweet_f,'w')
	in_file = open(in_file_f,'w')
	
	new_tweet.write("1")
	in_file.write(str(itr))
		
