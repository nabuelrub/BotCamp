
# coding: utf-8

# In[7]:



import codecs
import os, sys
import numpy as np
import datetime
from igraph import *
import itertools
from pybloom import BloomFilter

users = []

users40k = BloomFilter(capacity=50000, error_rate=0.0000001)

filepath = open(os.path.join('ParsedData', 'bots.csv'))
for i in filepath:
    i = i.rsplit("\n")[0]
    users40k.add(i)
filepath.close()


f = codecs.open(os.path.join('ParsedData', 'userInfo.csv'),"r","utf-8")
for i in f:
    i = i.rsplit("\n")[0]
    i = i.rsplit("\t")
    if i[1] in users40k:
        users.append([i[1],i[2]])
    
f.close()



# In[ ]:




# In[8]:

allusers = []
for i in users:
    allusers.append(i[0])
allusers = list(set(allusers))


# In[9]:

dicusers = {}
for  j, i in enumerate(allusers):
    dicusers[i]= j


# In[ ]:




# In[10]:

edges = []
visited = BloomFilter(capacity=len(users)*10, error_rate=0.0000001)
for i in range(0,len(users)):
    for j in range(i+1,len(users)):
        if users[i][1] == users[j][1] and users[i][0] != users[j][0]  and str([users[i][0],users[j][0]]) not in visited and  str([users[j][0],users[i][0]]) not in visited :
            sortedL = sorted([dicusers[users[i][0]], dicusers[users[j][0]]])
            edges.append(zip([sortedL[0]],[sortedL[1]])[0])
            visited.add(str([users[i][0],users[j][0]]))

print len(allusers)
print len(edges)

# In[13]:

g = Graph(len(allusers),edges=edges, directed=False)
g.vs["user_id"] = [i for i in allusers]
filepath = open(os.path.join('ParsedData', 'temporal_clusters.csv'),'w')
community = g.community_multilevel()
for i in range(0,len(community.membership)): 
    filepath.write(str(allusers[i])+","+str(community.membership[i])+"\n")
filepath.close()

g.write_gml("clusters.gml")
'''from collections import Counter
print Counter(community.membership)
'''