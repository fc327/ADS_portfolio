
# coding: utf-8

# In[56]:


import numpy as np
import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.model_selection import train_test_split
from sklearn.decomposition import LatentDirichletAllocation


# In[3]:


yt_dislikes = pd.read_csv('youtube_dislike_dataset.csv')
yt_dislikes.head()


# In[4]:


yt_dislikes.columns


# In[5]:


# finding any missing values in each column of the data frame 
# the only column where there is missing data is in the 'comments' column 

yt_dislikes.isna().sum()


# In[6]:


# dropping columns that are irrelevant to the analysis 

yt_dislikes.drop(['video_id', 'channel_id'], axis = 1, inplace = True)


# In[7]:


# this only provides a description for numerical data 

yt_dislikes.describe()


# In[8]:


yt_dislikes['tags'][500]


# In[10]:


yt_dislikes.head()


# In[11]:


# as the data description on kaggle indicated, the comments field in this dataset
# has 20 random comments for each video (not necessarily in sequential order)

yt_dislikes['comments'][500]


# In[12]:


type(yt_dislikes['tags'][500])


# In[13]:


yt_dislikes.channel_title.unique()


# In[14]:


# data from 10,883 different YouTube channels 

len(yt_dislikes.channel_title.unique())


# In[16]:


# an example of what the tags look like in each record of the data set 
yt_dislikes['tags'][0]


# In[17]:


from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

wordcloud = WordCloud().generate(yt_dislikes['tags'][0])

# Display the generated image:
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")

plt.show()


# In[18]:


# the full list of youtube channels
# the output is hidden, but to open/close do command + M + O 

yt_dislikes['channel_title'].unique().tolist()


# In[19]:


# the most frequent channel title in this data set 
# can be called using the built-in .mode() function

yt_dislikes['channel_title'].mode()


# In[20]:


# this code shows the number of occurrences of the channel title in this data set 
# for example, there are 533 observations of the channel 'Sky Sports Football' 
# ironically, the 5 highest number of observations are all sports channels  

yt_dislikes['channel_title'].value_counts()


# In[21]:


# this is a way to combine all the records for the top 5 channels (in terms of frequency)

yt_sports_channels = yt_dislikes.loc[(yt_dislikes['channel_title'] == 'Sky Sports Football') | (yt_dislikes['channel_title'] == 'The United Stand') | 
                                     (yt_dislikes['channel_title'] == 'BT Sports') | (yt_dislikes['channel_title'] == 'NBA') |
                                     (yt_dislikes['channel_title'] == 'NFL')]
yt_sports_channels.head()


# In[22]:


# total number of observations in the new dataframe 

len(yt_sports_channels)


# In[23]:


yt_sports_channels.sort_values(by = 'dislikes', ascending = False)


# In[24]:


# this is how to calculate the like percentage on each video 

yt_sports_channels['likes'][6396]/(yt_sports_channels['likes'][6396] + yt_sports_channels['dislikes'][6396])


# In[25]:


yt_sports_channels['like%'] = yt_sports_channels['likes']/(yt_sports_channels['likes'] + yt_sports_channels['dislikes'])
yt_sports_channels.tail()


# In[26]:


yt_sports_channels.sort_values(by = 'like%', ascending = False)


# In[27]:


yt_sports_channels['comments'][36659]


# In[28]:


import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity


# In[30]:


wc0 = WordCloud().generate(yt_sports_channels['comments'][36659])

plt.imshow(wc0, interpolation = 'bilinear')
plt.axis("off")

plt.show()


# In[36]:


# the 'drop = True' command drops the old index values 
# 'inplace = True' makes sure to not change the 

yt_sports_channels.reset_index(drop = True, inplace = True)


# In[37]:


yt_sports_channels.tail()


# In[32]:


# showing number of missing values in each column in the yt_sports_channels dataframe

yt_sports_channels.isna().sum()


# In[38]:


yt_sports_channels['comments'][0]


# In[39]:


# trying out regular expressions for the text data (comments) in this dataset 

import re
re_word = re.compile('\w+')
print(re.findall, re_word, yt_sports_channels['comments'][0])


# In[ ]:


nltk.download('punkt')

nltk.word_tokenize(yt_sports_channels['comments'][0])


# In[42]:


# creating different vectorizers 

unigram_count_vect = CountVectorizer(encoding = 'latin-1', binary = False, min_df = 5, stop_words = 'english')
unigram_tfidf_vect = TfidfVectorizer(encoding = 'latin-1', use_idf = True, min_df = 5, stop_words = 'english')


# In[61]:


X = yt_sports_channels['comments'].values
y = yt_sports_channels['tags'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)
print(X_train[0])
print(y_train[0])
print(X_test[0])
print(y_test[0])


# In[88]:


tfidf_vecs = unigram_tfidf_vect.fit_transform(X_train)
print(list(unigram_tfidf_vect.vocabulary_.items())[:10])


# In[52]:


# mnb = MultinomialNB()
# mnb.fit(tfidf_vecs, y_train)


# In[50]:


v_feature_names = unigram_tfidf_vect.get_feature_names_out()


# In[51]:


terms =  list(unigram_tfidf_vect.get_feature_names_out())
print("Vocabulary has %d distinct terms" % len(terms))


# In[53]:


def termrankings(tfidf_vecs, terms):
  sums = tfidf_vecs.sum(axis=0)
  # map weights to the terms
  weights = {}
  for col, term in enumerate(terms):
    weights[term] = sums[0,col]
  # rank the terms by their weight
  return sorted(weights.items(), key = operator.itemgetter(1), reverse = True)


# In[55]:


import operator # the following error would occur if not imported: "operator not defined"

ranking = termrankings(tfidf_vecs, terms)
for i, pair in enumerate(ranking[0:50]):
    print( "%02d. %s (%.2f)" % (i+1, pair[0], pair[1] ))


# In[57]:


lda = LatentDirichletAllocation(n_components = 20, max_iter = 5, 
    learning_method = 'online', learning_offset = 50, random_state = 0)
lda_transformed = lda.fit_transform(tfidf_vecs)


# In[58]:


def display_topics(model, feature_names, topwords):
  for top_id, topic in enumerate(model.components_):
    print("Topic %d:" % (top_id))
    print(" ".join([feature_names[i] for i in topic.argsort()[:-topwords - 1:-1]]))

words = 10
display_topics(lda, v_feature_names, words)


# In[60]:


print(lda_transformed.shape)
print(lda_transformed[0])


# In[85]:


# using the tfidf vectorizer on the y_train data which has the values from the 'tags' column 

tfidf_vecs2 = unigram_tfidf_vect.fit_transform(y_train)
print(list(unigram_tfidf_vect.vocabulary_.items())[:10])


# In[66]:


lda2 = LatentDirichletAllocation(n_components = 20, max_iter = 10, 
    learning_method = 'online', learning_offset = 50, random_state = 0)
lda_transformed2 = lda2.fit_transform(tfidf_vecs2)


# In[67]:


display_topics(lda2, v_feature_names, words)


# In[68]:


print(lda_transformed2.shape)
print(lda_transformed2[0])


# In[79]:


wordcloud = WordCloud(width = 3000, height = 2000, random_state = 1,
background_color = 'white', colormap = 'rainbow', collocations = False,
stopwords = STOPWORDS).generate(X_train[50])

# Display the generated image:
plt.figure(figsize=(20,10))
plt.imshow(wordcloud)
plt.axis("off")

plt.show()

