
# coding: utf-8

# In[32]:



import os
import codecs 
import sys

path = str(sys.argv[1])
filepath = open(os.path.join('ParsedData', 'userInfo.csv'))
data = []
for i in filepath:
    i = i.rsplit("\n")[0]
    i = i.rsplit("\t")
    data.append(i)
print len(data), data[0]
filepath.close()


dic = {}
clusters = [i[2] for i in data]
clusters = list(set(clusters))
print len(clusters)

for i in clusters:
    dic[i] = []
for i in data:
    dic[i[2]].append(i[1])


# In[33]:

data = []
users = set()
f = codecs.open(os.path.join('ParsedData', 'features_bots.csv'),"r","utf-8")
for i in f:
    i = i.rsplit("\n")[0]
    i = i.rsplit("\t")
    if len(i) <24:
        continue
    data.append([i[4],i[2],i[24]])
    users.add(str(str(i[24])+'_'+str(i[4])))
f.close()


# In[ ]:

'''
sql='SELECT user_id, txt, round from tweets_bots '
r = cur.execute(sql)
print cur.rowcount
cursor = cur.fetchall()
data = []
users = set()
for i in cursor:
    data.append([i[0],i[1],i[2]])
    users.add(str(str(i[2])+'_'+str(i[0])))
db.close()
'''


# In[34]:

print len(data)
print data[0]


# In[35]:


pol = {}
for i in users:
    if i == 0:
        continue
    pol[i] = []
for i in data:
    if i[0] ==0:
        continue
    pol[str(str(i[2])+'_'+str(i[0]))].append(i[1].lower())
    


# In[13]:




# In[36]:
import nltk
nltk.download('stopwords')
from nltk import ngrams
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import stop_words
from stop_words import get_stop_words
nltk.download('punkt')

stop = stopwords.words('english')+list(string.punctuation)
stop.append(u'"')
stop.append(u'``')
stop.append(u"''")
stop.append(u'rt')
stop.append(u'https')
n = 1
cluster_similarity = {}
for k, v in dic.iteritems():  
    #print k,  v
    try: 
        pol[str(k)[0:-4]+'_'+str((v[0]))]
    except:
        print sys.exc_info()[0]
        continue
    grams = []
    for u in range(0,len(v)):
        grams.append([])
        try:
            for sentence in pol[str(k)[0:-4]+'_'+str((v[u]))]:
                s = sentence.lower()
                sentence = s#.decode('utf-8')     
                sixgrams = ngrams([i for i in word_tokenize((sentence.lower())) if i not in stop ],n)

                for gram in sixgrams:
                  grams[u].append(gram)
            
        except:
                print sys.exc_info()[0]
                continue
            
    sim = 0
    for i in range(0, len(grams)):
        for j in range(i+1, len(grams)):
            if len(( set(grams[i]).union(set(grams[j])))) == 0:
                sim += 0
            else:
                sim+=float(len(list( set(grams[i]).intersection(set(grams[j])))))/ len(( set(grams[i]).union(set(grams[j]))))

    cluster_similarity[k] = (float(sim)/((len(v)-1)*len(v)/2))


# In[37]:

users_gthan = set()
for k, i in cluster_similarity.iteritems():
    if i>=0.5:
        for j in dic[k]:
            users_gthan.add(j)
print len(users_gthan)
users_gthan = list(users_gthan)


# In[38]:

filepath = open(os.path.join('ParsedData', 'dynamics.csv'),'w')
for k, v in cluster_similarity.iteritems():
    filepath.write(str(k)+"\t"+str(v)+"\n")
filepath.close()

filepath = open(os.path.join('ParsedData', 'bots.csv'),'w')
for i in users_gthan:
    filepath.write(i+"\n")
filepath.close()


# In[39]:

hashtags  = []
for line in open(os.path.join(path, 'keywords.txt'),'r'):
    hashtags.append(line.split('\n')[0].lower())
hashtags = [i.replace('#','') for i in hashtags ]


# In[40]:

from nltk import ngrams
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
import sys

stop = stopwords.words('english') + list(string.punctuation)
stop.append(u'"')
stop.append(u'``')
stop.append(u"''")
stop.append(u'rt')
stop.append(u'https')
n = 1
cluster_similarity = {}
for k, v in dic.iteritems():  
    try:
        pol[str(k)[0:-4]+'_'+str((v[0]))]
    except:
        print sys.exc_info()[0]
        continue
    grams = []
    for u in range(0,len(v)):
        grams.append([])
        try:
            for sentence in pol[str(k)[0:-4]+'_'+str((v[u]))]:
                s = sentence.lower()
                sentence = s #.decode('utf-8')     
                sixgrams = ngrams([i for i in list(set(word_tokenize((sentence.lower()))).intersection(set(hashtags))) ],n)

                for gram in sixgrams:
                  grams[u].append(gram)

        except:
            print sys.exc_info()[0]
            continue
            
    sim = 0
    for i in range(0, len(grams)):
        for j in range(i+1, len(grams)):
            if len(( set(grams[i]).union(set(grams[j])))) == 0:
                sim += 0
            else:
                sim+=float(len(list( set(grams[i]).intersection(set(grams[j])))))/ len(( set(grams[i]).union(set(grams[j]))))

    cluster_similarity[k] = (float(sim)/((len(v)-1)*len(v)/2))


# In[41]:

users_gthan2 = set()
for k, i in cluster_similarity.iteritems():
    if i>=0.5:
        for j in dic[k]:
            users_gthan2.add(j)
print len(users_gthan2)
users_gthan2 = list(users_gthan2)


# In[42]:

filepath = open(os.path.join('ParsedData', 'dynamics_hashtags.csv'),'w')
for k, v in cluster_similarity.iteritems():
    filepath.write(str(k)+"\t"+str(v)+"\n")
filepath.close()

filepath = open(os.path.join('ParsedData', 'bots.csv'),'a')
for i in users_gthan2:
    if i not in users_gthan:
        filepath.write(i+"\n")
filepath.close()


# In[ ]:



