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

visited = []
main_path = path+'/data' #copy the address of a directory that all w* data are there
counter = 0
s= "\t"
features = codecs.open(os.path.join('ParsedData', 'features.csv'),'w',"utf-8")

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
							fileName = rounds[0] + '/' + '1.txt'
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

						files = find_files(rounds[0],'[1..20].txt')
						w1 = rounds[0].find('w')
						w2 = rounds[0].find('/Night')
						n = rounds[0].rfind('/')
						RoundNum = 100000+int(rounds[0][w1+1:w2])*1000 +int(rounds[0][n-1:n])*100+int(rounds[0][n+7:])
						print 'Round num',RoundNum
						RoundNum = str(RoundNum)

						for f in files:
							tweet_file = codecs.open(f,'r',encoding="utf-8")
							print f
							for line in tweet_file:
								try:
									twt = json.loads(line)
									#------------------example of extracting data from a tweet
									if 'created_at' in twt:
										screen_name = twt['user']['screen_name']
									
										created_at = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(twt['created_at'],'%a %b %d %H:%M:%S +0000 %Y'))
									
										ID = twt['id_str']
										
										text =  twt['text'] if twt['text'] != None else u""
										text = text.replace("\t"," ").replace('\n', ' ').replace('\r', ' ')
										source = twt['source'] if twt['source'] != None else u""
										pos1 = source.find(">")
										pos2 = source.rfind("<")
										source = source[pos1+1:pos2]
										user_id = twt['user']['id_str'] if twt['user']['id_str']!= None else u""
										
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
											features.write(ID+s+created_at+s+text+s+source+s+user_id+s+user_name+s+user_screen_name+s+user_location+s+user_url+s+user_description+s+str(user_verified)+s+str(user_followers_count)+s+str(user_friends_count)+s+str(user_listed_count)+s+str(user_favourites_count)+s+str(user_statuses_count)+s+str(user_created_at)+s+user_lang+s+str(longtitude)+s+str(latitude)+s+str(retweeted_user_id)+s+retweeted_user_screen_name+s+lang+s+str(timestamp_ms)+s+RoundNum+"\n")
										else:
											features.write(ID+s+created_at+s+text+s+source+s+user_id+s+user_name+s+user_screen_name+s+user_location+s+user_url+s+user_description+s+str(user_verified)+s+str(user_followers_count)+s+str(user_friends_count)+s+str(user_listed_count)+s+str(user_favourites_count)+s+str(user_statuses_count)+s+str(user_created_at)+s+user_lang+s+str(longtitude)+s+str(latitude)+s+u""+s+u""+s+lang+s+str(timestamp_ms)+s+RoundNum+"\n")
									
										'''if len(line) > 100:
											print line
										if '"delete":{' in line:
											status = twt['status']if twt['status'] != None else u""
											status = status.replace("\t"," ").replace('\n', ' ').replace('\r', ' ')
											id_str = twt['id_str']if twt['id_str'] != None else u""
											user_id_str = twt['user_id_str']if twt['user_id_str'] != None else u""
											delete.write(status+s+id_str+s+user_id_str+"\n")'''


								except:
									print "Error parsing"
									e=sys.exc_info()[0]
									

						

								



