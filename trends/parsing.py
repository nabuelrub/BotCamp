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
from collections import Counter



#source = sys.argv[1]
destination = sys.argv[1]
dir_path = sys.argv[1]

def find_files(directory, pattern):
	for root, dirs, files in os.walk(directory):
		dirs.sort()
		for basename in files:
			if fnmatch.fnmatch(basename, pattern):
				filename = os.path.join(root, basename)
				yield filename

count = 1
typetwt = str(0)			
visited = []
#main_path = '/nfs/election/Dynamic Listening/code/w1/' #copy the address of a directory that all w* data are there
counter = 0
s= "\t"

copyf = codecs.open(dir_path+'/keywords.txt','r',"utf-8")	
keywords = []				
for i in copyf:
	keywords.append((i.rsplit("\n")[0]).lower())
copyf.close()


ftrends = codecs.open(destination+'/trends.txt','r',"utf-8")
trends = []
for i in ftrends:
	if ((i.rsplit(",")[0]).lower()) not in keywords:
		trends.append((i.rsplit("\n")[0]).lower())
		#print 'adding',(i.rsplit("\n")[0]).lower()


#print len(trends),trends[0]

freq = []
freqPolitical = []
for i,j in enumerate(trends):
	#dic[j]=i
	freq.append(0)
	freqPolitical.append(0)
files = find_files(destination,'[1-20].txt')
num_twt = 0
hashtag=[]

for f in files:
	print 'reading',f
	tweet_file = open(f,'r')
	for line in tweet_file:
		#if count >= 200:
		#	break
		try:
			twt = json.loads(line)
			
			#------------------example of extracting data from a tweet

			if 'created_at' in twt:
				txt = twt['text']
				txt = txt.lower()
				num_twt = num_twt+1
				 
				for i,j  in enumerate(trends):
					if j in txt :
						 
						freq[i]=freq[i]+1
						if any(ii in txt for ii in keywords):
							freqPolitical[i] = freqPolitical[i] +1

						
		except:
			print "Error parsing"
			e=sys.exc_info()[0]
			#print 
			print e
	tweet_file.close()

print freq
print num_twt
adding = []
finfo = codecs.open(destination+"/trends_statistics.txt",'w',"utf-8")
for i,j in enumerate(freq):
	if j > 0:
		#print trends[i], j ,freqPolitical[i]/float(j)
		finfo.write(trends[i]+' '+str(j)+' '+str(freqPolitical[i])+' '+str(freqPolitical[i]/float(j))+'\n')
		if freqPolitical[i]/float(j) >= .50:
			print 'adding',trends[i],j , freqPolitical[i], freqPolitical[i]/float(j)
			adding.append(trends[i])
	

trendw = open(dir_path+'/trendwriting.txt','w')
trendw.write('1')	
trendw.close()

trends_old = []
copyf = codecs.open(dir_path+'/trends.txt','r','utf-8')					
for i in copyf:
	trends_old.append(i.rsplit("\n")[0])
copyf.close()

trends_new = trends_old + adding
trends_new = trends_new[-400:]

copyf = codecs.open(dir_path+'/trends.txt','w','utf-8')					
for i in trends_new:
	copyf.write(i+"\n")

copyf.close()



trendw = open(dir_path+'/trendwriting.txt','w')
trendw.write('0')	
trendw.close()



