
# coding: utf-8

# In[3]:

import codecs
import os, sys
import numpy as np
import datetime
from igraph import *
import itertools
from pybloom import BloomFilter


users = []
all_users_40 = []

users40k = BloomFilter(capacity=50000, error_rate=0.0000001)

filepath = open(os.path.join('ParsedData', 'bots.csv'))
for i in filepath:
    i = i.rsplit("\n")[0]
    users40k.add(i)
    all_users_40.append(i)
filepath.close()

f = open(os.path.join('ParsedData', 'media_edges.txt'),'r')
for i in f:
    i = i.rsplit("\n")[0]
    i = i.rsplit("\t")
    if i[0] in users40k and i[1] in users40k and  i[0] <> i[1]:
        users.append([i[0],i[1]])
f.close()


# In[4]:

busers = BloomFilter(capacity=len(users)+10, error_rate=0.0000001)
for i in users:
    busers.add(str(i))
edges = []
for i in users:
    edges.append([i[0],i[1]])

users = edges
users =sorted(users)
users = list(users for users,_ in itertools.groupby(users))


# In[5]:


allusers = list(set(all_users_40))


# In[6]:

dicusers = {}
for  j, i in enumerate(allusers):
    dicusers[i]= j


# In[7]:

from pybloom import BloomFilter
busers = BloomFilter(capacity=len(users)+10, error_rate=0.0000001)
for i in users:
    busers.add(str(i))


# In[8]:

edges = []
weight = []
for i in users:
    sortedL = sorted([dicusers[i[0]],i[1], dicusers[i[1]]])
    edges.append(zip([sortedL[0]],[sortedL[1]])[0])



# In[9]:

g = Graph(len(allusers),edges=edges, directed=False)


# In[10]:


g.vs["user_id"] = [i for i in allusers]


# In[9]:




# In[11]:




# In[12]:
#
#g.write_gml("reweets.gml")


# In[21]:

filepath = open(os.path.join('ParsedData', 'media_clusters.csv'),'w')
community = g.community_multilevel()
for i in range(0,len(community.membership)): 
    filepath.write(str(allusers[i])+","+str(community.membership[i])+"\n")
filepath.close()

