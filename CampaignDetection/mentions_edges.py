import csv
import json
import sys
import io
import codecs
import re
import fnmatch
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

pair = []
output = codecs.open(os.path.join('ParsedData', 'mentions_edges.txt'),'w',"utf-8")
f = codecs.open(os.path.join('ParsedData', 'mentions.csv'),'r',"utf-8")
for i in f:
	i = i.rsplit("\t")
	#print len(i)
	if i[7] == "":
		if i[2] in bfilter :
			if i[5] in bfilter:
				pair.append([i[2],i[5]])
str_pair = [str(i[0]+","+i[1]) for i in pair]
str_pair = list(set(str_pair))
pair = [[i.rsplit(",")[0],i.rsplit(",")[1]] for i in str_pair]

for i in pair:
	if [i[1],i[0]] in pair:
		output.write(i[0]+"\t"+i[1]+"\n")

