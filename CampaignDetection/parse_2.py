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


typetwt = str(0)			
visited = []
path = str(sys.argv[1])

main_path = path+'/data' #copy the address of a directory that all w* data are there
counter = 0
s= "\t"
features = codecs.open(os.path.join('ParsedData', 'features_bots.csv'),'w',"utf-8")
userInfo = codecs.open(os.path.join('ParsedData', 'userInfo.csv'),'w',"utf-8")

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
						ParsedData = 100000+int(rounds[0][w1+1:w2])*1000 +int(rounds[0][n-1:n])*100+int(rounds[0][n+7:])
						print 'Round num',ParsedData
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
								dicCluster[bot_arr[i][j]] = ParsedData*10000+ClusterCount
								dicUsers[bot_arr[i][j]] = ""
								#print ParsedData*10000+ClusterCount
								
						cap = len(bot_list) if len(bot_list) > 0 else 1
						bfilter = BloomFilter(capacity=cap, error_rate=0.0001)	
						for i in range (len(bot_arr)):
							for j in range (len(bot_arr[i])):
								bfilter.add(bot_arr[i][j])	

						for line in tweet_file:
							try:
								twt = json.loads(line)
								#------------------example of extracting data from a tweet
								if 'created_at' in twt:
									screen_name = twt['user']['screen_name']
									if screen_name in bfilter:
										created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(twt['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
										#print 'date',created_at

										#print screen_name
										#text =  str(twt['text'].encode('utf-8'))
										#source = str(twt['source'].encode('utf-8'))
										ID = twt['id_str']
										
										text =  twt['text'] if twt['text'] != None else u""
										text = text.replace("\t"," ").replace('\n', ' ').replace('\r', ' ')
										source = twt['source'] if twt['source'] != None else u""
										pos1 = source.find(">")
										pos2 = source.rfind("<")
										source = source[pos1+1:pos2]
										user_id = twt['user']['id_str'] if twt['user']['id_str']!= None else u""
										dicUsers[screen_name] = user_id
										#user_name = str(twt['user']['name'].encode('utf-8'))
										#user_screen_name = str(twt['user']['screen_name'].encode('utf-8'))
										user_name = twt['user']['name'] if twt['user']['name'] != None else u""
										user_name = user_name.replace("\t"," ").replace('\n', ' ').replace('\r', ' ')
										user_screen_name = twt['user']['screen_name'] if twt['user']['screen_name']!= None else u""
										#print twt['user']['location']
										user_location= twt['user']['location'] if twt['user']['location'] != None else u""
										user_location = user_location.replace("\t"," ").replace('\n', ' ').replace('\r', ' ')

										user_url= twt['user']['url'] if twt['user']['url'] != None else u""
										user_description= twt['user']['description'] if twt['user']['description']  != None else u""
										user_description = user_description.replace("\t"," ").replace('\n', ' ').replace('\r', ' ')

										user_verified= twt['user']['verified'] if twt['user']['verified'] != None else u""
										user_followers_count= twt['user']['followers_count'] if twt['user']['followers_count'] != None else u""
										user_friends_count= twt['user']['friends_count'] if twt['user']['friends_count'] != None else u""
										user_listed_count= twt['user']['listed_count']if twt['user']['listed_count'] != None else u""
										user_favourites_count= twt['user']['favourites_count'] if twt['user']['favourites_count'] != None else u""
										user_statuses_count= twt['user']['statuses_count'] if twt['user']['statuses_count'] != None else u""
										user_created_at= time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(twt['user']['created_at'],'%a %b %d %H:%M:%S +0000 %Y')) if twt['user']['created_at'] != None else u""
										user_lang= twt['user']['lang'] if twt['user']['lang'] != None else u""
										#user_image_profile= twt['user']['image_profile']
										coordinates= twt['coordinates'] if twt['coordinates'] != None else u""
										if coordinates != u"":
											longtitude = coordinates['coordinates'][0]
											latitude = coordinates['coordinates'][1]
										else:
											longtitude = u""
											latitude = u""

										place= twt['place'] if twt['place']!= None else u"" 
										retweeted = False
										if 'retweeted_status' in twt:
											retweeted = True
											retweeted_user_id = twt['retweeted_status']['user']['id']  if twt['retweeted_status']['user']['id'] != None else u""
											retweeted_user_screen_name = twt['retweeted_status']['user']['screen_name'] if twt['retweeted_status']['user']['screen_name'] != None else u""
										lang= twt['lang'] if twt['lang']  != None else u""
										timestamp_ms= twt['timestamp_ms'] if twt['timestamp_ms'] != None else u""
										if retweeted:
											features.write(ID+s+created_at+s+text+s+source+s+user_id+s+user_name+s+user_screen_name+s+user_location+s+user_url+s+user_description+s+str(user_verified)+s+str(user_followers_count)+s+str(user_friends_count)+s+str(user_listed_count)+s+str(user_favourites_count)+s+str(user_statuses_count)+s+str(user_created_at)+s+user_lang+s+str(longtitude)+s+str(latitude)+s+str(retweeted_user_id)+s+retweeted_user_screen_name+s+lang+s+str(timestamp_ms)+s+str(ParsedData)+"\n")
										else:
											features.write(ID+s+created_at+s+text+s+source+s+user_id+s+user_name+s+user_screen_name+s+user_location+s+user_url+s+user_description+s+str(user_verified)+s+str(user_followers_count)+s+str(user_friends_count)+s+str(user_listed_count)+s+str(user_favourites_count)+s+str(user_statuses_count)+s+str(user_created_at)+s+user_lang+s+str(longtitude)+s+str(latitude)+s+u""+s+u""+s+lang+s+str(timestamp_ms)+s+str(ParsedData)+"\n")
						
							except:
								print "Error parsing"
								


						# end for loop
						ClusterCount = 0
						for i in range (len(bot_arr)):
							ClusterCount = ClusterCount+1
							for j in range (len(bot_arr[i])):
								userInfo.write(bot_arr[i][j]+s+dicUsers[bot_arr[i][j]]+s+str(ParsedData*10000+ClusterCount)+s+str(ParsedData)+"\n")

								



