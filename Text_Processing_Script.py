
# coding: utf-8

# In[1]:

#!/usr/bin/python3

def GetHTML(urL):
    import requests
    from lxml import html 
    return html.fromstring((requests.get(url)).text)

url = "https://www.wired.com/"
wired_html = GetHTML(url)

###create the array to hold on to all the headlines
headlines_array = []

### the headline will be the document #####

for i in range(0,49):
    headlines = '//*[(@id = "security-card")]//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))] | //*[(@id = "science-card")]//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))] | //*[(@id = "business-card")]//*[contains(concat( " ", @class, " " ), concat( " ", "title", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "clamp-6", " " ))] | //*[(@id = "most-pop-list")]//*[contains(concat( " ", @class, " " ), concat( " ", "exchange-sm", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "inline-block", " " )) and contains(concat( " ", @class, " " ), concat( " ", "isActive", " " ))] | //*[(@id = "latest-news-list")]//*[contains(concat( " ", @class, " " ), concat( " ", "line-clamp", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "clamp-5", " " ))] | //*[contains(concat( " ", @class, " " ), concat( " ", "clamp-3", " " ))]'
    headlines = wired_html.xpath(headlines)[i].text_content()
    headlines_array.append(headlines)




# In[2]:

for i in range(0,49):
    print(headlines_array[i])
    




# In[3]:

### we are going to seperate the headlines into two topics: cultural headlines and tech headlines

target_headlines_index = {2,4,5,7,16,22,26,27,31,32,34,36}
target_headlines = []

for i in target_headlines_index:
    target_headlines.append(["pos", headlines_array[i]])

# use this to get the rest of the headlines
nontarget_headlines = []
for j in range(0,49):
    if j not in target_headlines_index:
        nontarget_headlines.append(["neg",headlines_array[j]])
        
#merge the two lists now
data = target_headlines + nontarget_headlines


# In[4]:

data[5][1]


# In[5]:

import nltk
from nltk.corpus import stopwords
import random
stop_words = stopwords.words('english')

def features(sentence):
    features = dict()
    tokens = nltk.word_tokenize(sentence)
    pos_tagged_tokens = nltk.pos_tag(tokens)
    for token, pos_tag in pos_tagged_tokens:
        # We keep only specific part of speech as features
        if (pos_tag.startswith("NNP")):
            features[token+"/"+pos_tag] = True
    return features


# In[6]:

#labeled_features = []

#for i in range(0,49):
 #   labeled_features.append(features(data[i][1]))
    
labeled_features = [(features(sent), tag) for (tag, sent) in data]


# In[7]:

labeled_features


# In[8]:

import random

trials = 10
psum = 0;
cnt = 0;
for i in range(trials):
    random.shuffle(labeled_features)
    train_set, test_set = labeled_features[30:], labeled_features[:30]
    classifier = nltk.NaiveBayesClassifier.train(train_set)
    accuracy = nltk.classify.accuracy(classifier, test_set)
    print("Trial:", cnt, " Accuracy:", accuracy)
    psum += accuracy
    cnt += 1
    
print("Avg Accuracy: ", (psum/cnt))


# In[9]:

classifier = nltk.NaiveBayesClassifier.train(train_set)


# In[10]:

classifier.show_most_informative_features(30)


# In[11]:

import math
f  = classifier._feature_probdist
mif = classifier.most_informative_features(30)
pos_features = []
neg_features = []
for (w,t) in mif:
    if t != True:
        continue
    p = f[("pos", w)]
    n = f[("neg", w)]
    l = p.logprob(t) - n.logprob(t)
    s = l/abs(l)
    word = w.split("/")[0]
    
    # print w, math.exp(abs(l)), s
    if s>0:
        pos_features.append(word)
    else:
        neg_features.append(word)


# In[12]:

set(neg_features) & set(pos_features)


# In[13]:

from wordcloud import WordCloud

pos_wordcloud = WordCloud().generate(" ".join(pos_features))
neg_wordcloud = WordCloud().generate(" ".join(neg_features))


# In[ ]:

get_ipython().magic('matplotlib inline')
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (15, 15)


# In[ ]:


plt.figure()
f, (ax1, ax2) = plt.subplots(2, 1, sharex=False, figsize=(15,10))
ax1.imshow(pos_wordcloud)
ax1.axis("off")
ax1.figsize=(15,10)
ax2.imshow(neg_wordcloud)
ax2.axis("off")

plt.axis("off")
plt.show()

