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

ID = set()
ID_dic = {}
ID_pair = []

output = codecs.open(os.path.join('ParsedData', 'media_edges.txt'),'w',"utf-8")
f = codecs.open(os.path.join('ParsedData', 'media.csv'),'r', "utf-8")
for i in f:
	i = i.rsplit("\t")
	#print len(i)
	if i[10] == "":
		if len(i) <5:
			print "skip"
			continue
		if i[2] in bfilter :
			ID.add(i[2])
			ID_pair.append([i[2],i[5]])
f.close()


for i in ID:
	ID_dic[i] = set()

for i in ID_pair:
	ID_dic[i[0]].add(i[1])

kk = [k for k,v in ID_dic.iteritems() if len(list(v)) < 2 ]
for i in kk:
	ID_dic.pop(i,None)

keys = ID_dic.keys()

for k in range(0,len(keys)):
	lv = list(ID_dic[keys[k]])
	for k2 in range(k+1,len(keys)):
		if (len(list(ID_dic[keys[k]].intersection((ID_dic[keys[k2]]))))) >= 1:
			output.write(keys[k]+"\t"+keys[k2]+"\n")
		
output.close()										
