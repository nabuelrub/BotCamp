
# coding: utf-8

# In[15]:

import os


bots = []
with open(os.path.join('ParsedData', 'user_diss.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        bots.append(row)
f.close()


clusters = []
with open(os.path.join('ParsedData', 'Clusters.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        clusters.append(row)
f.close()

bots_names = {}
with open(os.path.join('ParsedData', 'userInfo.csv')) as f:
    for row in f:
        row = row.rsplit("\n")[0]
        row = row.rsplit("\t")
        if row[1] in bots:
            bots_names[row[1]]=row[0]
f.close()



# In[16]:

filename =  open(os.path.join('ParsedData', 'campaigns.csv'),'w') 

for i in range(0,len(bots)):
    filename.write(bots[i]+","+bots_names[bots[i]]+","+clusters[i]+"\n")
filename.close()


# In[17]:




# In[ ]:



