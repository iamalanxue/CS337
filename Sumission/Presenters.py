#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import operator
import string
import nltk 
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.corpus import stopwords
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:


ALLAWARDS = [['best', 'picture', 'drama'], ['actor', 'actress'],
['best', 'picture', 'musical', 'comedy'], ['actor', 'actress'],
['best', 'picture', 'drama', 'actress'], ['actor'],
['best', 'picture', 'drama', 'actor'], ['actress'],
['best', 'picture', 'musical', 'comedy', 'actress'], ['actor'],
['best', 'picture', 'musical', 'comedy', 'actor'], ['actress'],
['best', 'picture', 'supporting', 'actress'], ['actor'],
['best', 'picture', 'supporting', 'actor'], ['actress'],
['best', 'director'], [],
['best', 'screenplay'], [],
['best', 'animated'], [],
['best', 'foreign', 'language'], [],
['best', 'score'], [],
['best', 'song'],[],
['best', 'drama', 'series'], [],
['best', 'musical', 'comedy', 'series'], [],
['best', 'television', 'picture'], ['actor', 'actress'],
['best', 'tv', 'picture', 'actress'], ['actor'], #discrepenacy might break in 2015
['best', 'television', 'picture', 'actor'], ['actress'] ,
['best', 'television', 'drama', 'series', 'actress'], ['actor'],
['best', 'tv', 'drama', 'actor'], ['actress'], #might break in 2015
['best', 'musical', 'comedy', 'series', 'tv', 'actress'], ['actor'],
['best', 'musical', 'comedy', 'series', 'tv', 'actor'], ['actress'],
['best', 'tv', 'supporting', 'actress'], ['actor'],
['best', 'tv', 'supporting', 'actor'], ['actress'],
['cecil', 'award'], []] 


# In[3]:


awardNames = [ 'best motion picture - drama', 
'best motion picture - comedy or musical', 
'best performance by an actress in a motion picture - drama', 
'best performance by an actor in a motion picture - drama', 
'best performance by an actress in a motion picture - comedy or musical', 
'best performance by an actor in a motion picture - comedy or musical', 
'best performance by an actress in a supporting role in a motion picture', 
'best performance by an actor in a supporting role in a motion picture', 
'best director - motion picture', 
'best screenplay - motion picture', 
'best animated feature film', 
'best foreign language film', 
'best original score - motion picture', 
'best original song - motion picture', 
'best television series - drama', 
'best television series - comedy or musical', 
'best mini-series or motion picture made for television', 
'best performance by an actress in a mini-series or motion picture made for television', 
'best performance by an actor in a mini-series or motion picture made for television', 
'best performance by an actress in a television series - drama', 
'best performance by an actor in a television series - drama', 
'best performance by an actress in a television series - comedy or musical', 
'best performance by an actor in a television series - comedy or musical', 
'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 
'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television',
'cecil b. demille award']


# In[4]:


categories = [ALLAWARDS[i] for i in range(0, len(ALLAWARDS), 2)]




def removePunc(x):
    x = re.sub(r'[@#]\w+', '', x) #taking out hashtags and @ 
    x = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', x) #taking out links 
    x = re.sub(r'[!?\.,\'\":()]+', '', x) #taking out punctuation i.e ? ! . ' and " 
    x = re.sub(r'(RT|rt) ', '', x) #taking out the initial "RT "
    x= re.sub(r'(g|G)olden (g|G)lobes*', '', x)
    return x.strip()




def findRows(x, contains, ncontains):
    s = "^"
    for word in contains:
        s += f'(?=.*{word})'
    for word in ncontains:
        s += f'(?!.*{word})'
    s += '.*$'
    if bool(re.match(s, x)):
        return True
    else:
        False
# con = ['best', 'screenplay']
# noncon = []
# df['Rows'] = df['text'].apply(lambda x: findRows(x, con, noncon))
# print(len(df))
# ccc = df[~df['Rows'].isnull()]
# print(len(ccc))


# In[10]:


def findPersonNames(text):
# text = 'Jessica Chastain so far is the best dressed Best body at the  ðŸ˜'
    text = text.title()
    names = []
    MAGIC_WORDS = ['Presents', 'Presenting', 'Presented', 'Introducing', 'Introduces', 'Awarding', 'Gives', 'Giving', 'Gave', 'Announce', 'Announcing']
    for w in MAGIC_WORDS:
        if len(text.split(w)) > 1:
            text = text.split(w)[0]
            break
    nltk_results = ne_chunk(pos_tag(word_tokenize(text)))
    for nltk_result in nltk_results:
        if type(nltk_result) == Tree:
            name = ''
            for nltk_result_leaf in nltk_result.leaves():
                if nltk_result_leaf[0] != 'Best':
                    name += nltk_result_leaf[0] + ' '
            names.append(name.strip())
#             print ('Type: ', nltk_result.label(), 'Name: ', name)
    return names


# In[11]:


def HASHGRAMS(df):
    df['ProperNouns'] = df['text'].apply(lambda x: findPersonNames(x))
    NGRAMS_DICT = {}
    for i in range(len(df)):
        PN = df['ProperNouns'].iloc[i]
        if len(PN) > 0: 
            for j in PN:
                if j == '': #take out empty string for some reason its added in there wack
                    continue
                name = j
                if len(name.split()) > 2:
                    multipleNames = name.split()
                    for n in range(0, len(multipleNames)-1, 2):
                        name = multipleNames[n] + ' ' + multipleNames[n+1]
                else:
                    name = j
                if name in NGRAMS_DICT:
                    NGRAMS_DICT[name] += 1
                else:
                    NGRAMS_DICT[name] = 1
    cd = sorted(NGRAMS_DICT.items(),key=lambda x: (x[1], len(x[0])),reverse=True)
    top2 = [l[0] for l in cd[0:2]]
    return top2
    
def makeDict(winners, awards):
    awardNames = {}
    for i in range(len(winners)):
        awardNames[awards[i]] = winners[i]
    return awardNames   



def presenter_names(year):
    if year=='2013':
        gg = pd.read_json('gg2013.json', orient='records')
    elif year=='2015':
        gg = pd.read_json('gg2015.json', orient='records')
    else:
        print("Wrong years")
        return
    
    copy = gg.copy(deep=True)
    copy['text'] = copy['text'].str.lower()
    copy['text'] = copy['text'].apply(lambda x: removePunc(str(x)))
    
    #takes out duplicate retweets 
    test = list(copy['text'].values)
    s = list(set(test))
    df = pd.DataFrame(s, columns=['text'])
        
    p = 0
    allpresenters = []
    for category in categories:
        con = category
        noncon = []
        df['Rows'] = df['text'].apply(lambda x: findRows(x, con, noncon))
        ccc = df[~df['Rows'].isnull()]
        dum = ccc.loc[ccc['text'].str.contains('presents') |
                ccc['text'].str.contains('presenting') | 
                ccc['text'].str.contains('presented') |
                ccc['text'].str.contains('introducing') |
                ccc['text'].str.contains('introduces') |
                ccc['text'].str.contains('introduced') |  
                ccc['text'].str.contains('awarding') | 
                ccc['text'].str.contains('gives') | 
                ccc['text'].str.contains('giving') |
                ccc['text'].str.contains('gave')  |
                ccc['text'].str.contains('announce') |
                ccc['text'].str.contains('announcing')
                ]
        if len(dum) > 0:
            presenters = HASHGRAMS(dum)
            allpresenters.append(presenters)
    #         print('subset of tweets filtered by category length: ', category , len(ccc))
    #         print('tweets with actual magic words: ', len(dum))
        else:
            presenters = []
            allpresenters.append(presenters)
    #1 and 2 suss 
    
    #THIS IS THE OUTPUT FOR PRESENTERS WHICH IS A DICTIONARY KEY: AWARD NAMES VALUE: LIST OF STRINGS 
    output = makeDict(allpresenters, awardNames)
    return output 
