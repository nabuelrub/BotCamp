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


hashtags  = []
path = str(sys.argv[1])
for line in open(os.path.join(path, 'keywords.txt'),'r'):
    hashtags.append(line.split('\n')[0].lower())
hashtags = [i.replace('#','') for i in hashtags ]


bots = []

filepath = open(os.path.join('ParsedData', 'bots.csv'))
for i in filepath:
    i = i.rsplit("\n")[0]
    bots.append(i)
filepath.close()

cap = len(bots) 
bfilter = BloomFilter(capacity=cap, error_rate=0.0000001)
for i in bots:
	bfilter.add(i)
output = codecs.open(os.path.join('ParsedData', 'hashtags_edges.txt'),'w',"utf-8")

ID = set()
ID_dic = {}
ID_pair = []
f = open(os.path.join('ParsedData', 'hashtags.csv'),'r')
for i in f:
	i = i.rsplit("\t")
	#print len(i)
	if i[6] == "":
		if i[4].lower() in hashtags:
			if len(i) <5:
				print "skip"
				continue
			if i[2] in bfilter :
				ID.add(i[2])
				ID_pair.append([i[2],i[4].lower()])
for i in ID:
	ID_dic[i] = set()



for i in ID_pair:
	ID_dic[i[0]].add(i[1])

keys = ID_dic.keys()
for k in range(0,len(keys)):
	lv = list(ID_dic[keys[k]])
	if len(lv)  == 0:
		continue
	for k2 in range(k+1,len(keys)):
		if len(list(ID_dic[keys[k2]])) >0 :
			if float(len(list(set(lv).intersection((ID_dic[keys[k2]])))))/len(list(set(lv).union((ID_dic[keys[k2]])))) >= 0.5 :
				output.write(keys[k]+"\t"+keys[k2]+"\n")
		
output.close()										
