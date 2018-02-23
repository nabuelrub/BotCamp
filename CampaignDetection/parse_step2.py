import csv
import json
import sys
import io
import codecs
import re
import fnmatch
#import MySQLdb
import os
import datetime, time
from pybloom import BloomFilter

def find_files(directory, pattern):
	for root, dirs, files in os.walk(directory):
		dirs.sort()
		for basename in files:
			if fnmatch.fnmatch(basename, pattern):
				filename = os.path.join(root, basename)
				yield filename

path = str(sys.argv[1])

typetwt = str(0)			
visited = []
main_path = path+'/data' #copy the address of a directory that all w* data are there
counter = 0
s= "\t"
fhashtags = codecs.open(os.path.join('ParsedData', 'hashtags.csv'),'a',"utf-8")
furls = codecs.open(os.path.join('ParsedData', 'urls.csv'),'a',"utf-8")
fmentions = codecs.open(os.path.join('ParsedData', 'mentions.csv'),'a',"utf-8")
fmedia = codecs.open(os.path.join('ParsedData', 'media.csv'),'a',"utf-8")


for weeks in os.walk(main_path):
	#print weeks
	if weeks[0].find('w') > 0:
		for nights in os.walk(weeks[0]):
			if nights[0].find('Night_') > 0:
				for rounds in os.walk(nights[0]):
					if rounds[0].find('Round') > 0:
						#------------------reading list of bot in the cluster
						#-------------------reading tweet file:
						tweet_file = []
						try:
							fileName = rounds[0] + '/' + 'reported_user_tweets.txt'
							if fileName not in visited:
								tweet_file = codecs.open(fileName,'r',encoding="utf-8")
								visited.append(fileName)
								print fileName
								
							else:
								continue

						except:
							print "Error file not found"
							e=sys.exc_info()[0]
							#print 
							print e

						files = find_files(rounds[0],'clstrs*ge_2.txt')
						w1 = rounds[0].find('w')
						w2 = rounds[0].find('/Night')
						n = rounds[0].rfind('/')
						RoundNum = 100000+int(rounds[0][w1+1:w2])*1000 +int(rounds[0][n-1:n])*100+int(rounds[0][n+7:])
						print 'Round num',RoundNum
						bot_list = []
						bot_arr = []
						for f in files:
							bot_file = open(f,'r')
							csv_reader = csv.reader(bot_file,delimiter=',',quotechar='\n')
							bot_arr = list(csv_reader) # this is 2D array, each row shows a cluster
						#print len(bot_arr)
						dicCluster = {}
						dicUsers = {}
						ClusterCount = 0
						for i in range (len(bot_arr)):
							ClusterCount = ClusterCount+1
							for j in range (len(bot_arr[i])):
								bot_list.append(bot_arr[i][j])	
								dicCluster[bot_arr[i][j]] = RoundNum*10000+ClusterCount
								dicUsers[bot_arr[i][j]] = ""
								#print RoundNum*10000+ClusterCount
								
						cap = len(bot_list) if len(bot_list) > 0 else 1
						bfilter = BloomFilter(capacity=cap, error_rate=0.0001)	
						for i in range (len(bot_arr)):
							for j in range (len(bot_arr[i])):
								bfilter.add(bot_arr[i][j])	

						for line in tweet_file:
							try:
								if len(line) < 100:
									continue
								twt = json.loads(line)
								#------------------example of extracting data from a tweet
								if 'created_at' in twt:
									screen_name = twt['user']['screen_name']
									if screen_name in bfilter:
										created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(twt['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
										ID = twt['id_str']
										user_id = twt['user']['id_str'] if twt['user']['id_str']!= None else u""
										dicUsers[screen_name] = user_id
										user_screen_name = twt['user']['screen_name'] if twt['user']['screen_name']!= None else u""
										retweeted_user_id = ''
										if 'retweeted_status' in twt:
											retweeted_user_id = twt['retweeted_status']['user']['id']  if twt['retweeted_status']['user']['id'] != None else u""
										timestamp_ms= twt['timestamp_ms'] if twt['timestamp_ms'] != None else u""
										######## hashtags #########
										for i in twt['entities']['hashtags']:
											fhashtags.write(ID+s+created_at+s+user_id+s+user_screen_name+s+i['text']+s+str(timestamp_ms)+s+str(retweeted_user_id)+s+str(dicCluster[screen_name])+s+str(RoundNum)+"\n")
										######## urls #########
										for i in twt['entities']['urls']:
											furls.write(ID+s+created_at+s+user_id+s+user_screen_name+s+i['url']+s+str(timestamp_ms)+s+str(retweeted_user_id)+s+str(dicCluster[screen_name])+s+str(RoundNum)+"\n")
										######## mentions #########
										for i in twt['entities']['user_mentions']:
											fmentions.write(ID+s+created_at+s+user_id+s+user_screen_name+s+i['screen_name']+s+i['id_str']+s+str(timestamp_ms)+s+str(retweeted_user_id)+s+str(dicCluster[screen_name])+s+str(RoundNum)+"\n")
										######## media #########
										if 'media' in twt['entities']:
											for i in twt['entities']['media']:
												usr = '0'
												if 'source_user_id_str' in i:
													usr = i['source_user_id_str']
												fmedia.write(ID+s+created_at+s+user_id+s+user_screen_name+s+i['id_str']+s+i['media_url']+s+i['url']+s+i['type']+s+usr+s+str(timestamp_ms)+s+str(retweeted_user_id)+s+str(dicCluster[screen_name])+s+str(RoundNum)+"\n")
										
							except:
								print "Error parsing"
								