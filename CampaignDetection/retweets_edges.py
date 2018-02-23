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
fbots = codecs.open(os.path.join('ParsedData', 'bots.csv'),'r')
for i in fbots:
	i = i.rsplit("\n")[0]
	bots.append(i)
fbots.close()

cap = len(bots) 
bfilter = BloomFilter(capacity=cap, error_rate=0.0000001)
for i in bots:
	bfilter.add(i)

output = codecs.open(os.path.join('ParsedData', 'retweets_edges.csv'),'w',"utf-8")
f = codecs.open(os.path.join('ParsedData', 'features_bots.csv'),"r","utf-8")
for i in f:

	i = i.rsplit("\t")
	if len(i) <21:
		continue

	if i[20] != "":
		if i[4] in bfilter :
			if i[20] in bfilter:
				output.write(i[4]+"\t"+i[20]+"\n")
f.close()

f = codecs.open(os.path.join('ParsedData', 'features.csv'),"r","utf-8")
for i in f:

	i = i.rsplit("\t")
	if len(i) <20:
		continue
	if i[20] != "":
		if i[4] in bfilter :
			if i[20] in bfilter:
				output.write(i[4]+"\t"+i[20]+"\n")

								
f.close()
output.close()


