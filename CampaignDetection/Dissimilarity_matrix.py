
# coding: utf-8

# In[ ]:




# In[4]:


import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.cluster import KMeans
from collections import Counter




# In[16]:

features = {}

bots = set()
with open(os.path.join('ParsedData', 'retweets_clusters.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        row = row.rsplit(",")
        features[row[0]] = [row[1]]
        bots.add(row[0])
f.close()

with open(os.path.join('ParsedData', 'temporal_clusters.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        row = row.rsplit(",")
        features[row[0]].append(row[1])
f.close()

with open(os.path.join('ParsedData', 'hashtags_clusters.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        row = row.rsplit(",")
        features[row[0]].append(row[1])
f.close()

with open(os.path.join('ParsedData', 'media_clusters.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        row = row.rsplit(",")
        features[row[0]].append(row[1])
f.close()

with open(os.path.join('ParsedData', 'mentions_clusters.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        row = row.rsplit(",")
        features[row[0]].append(row[1])
f.close()



# In[20]:

similarity = []
data = features.values()
for i in range(0,len(data)):
    for j in range(i+1,len(data)):
        s = 0
        for k in range(0,5):
            if data[i][k] == data[j][k]:
                s=s+1
        similarity.append(s)


f = open(os.path.join('ParsedData', 'dissimilarity_matrix.csv'),"w")
for i in similarity:
    f.write(str(1- (float(i)/5))+"\n")
f.close()

f = open(os.path.join('ParsedData', 'user_diss.csv'),"w")
for i in features.keys():
    f.write(i+"\n")
f.close()