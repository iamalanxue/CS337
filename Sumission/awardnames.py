#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import copy
import operator
import string
import nltk 
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from nltk.corpus import stopwords


def removePunc(x):
    x = re.sub(r'[@#]\w+', '', x) #taking out hashtags and @ 
    x = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', x) #taking out links 
    x = re.sub(r'[!?\.,\'\":()]+', '', x) #taking out punctuation i.e ? ! . ' and " 
    x = re.sub(r'(RT|rt) ', '', x) #taking out the initial "RT "
    x= re.sub(r'(g|G)olden (g|G)lobes*', '', x)
    return x.strip()
# copy['text'] = copy['text'].str.lower()





# In[6]:


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


# In[8]:


def findAwards(text):
    award = ""
    firstsplit= text.split(' wins ', 1)
    if len(firstsplit) > 1:
        right = firstsplit[1].split()
        try:
            bestIndex = right.index('Best') #start at this index right so my first word will always be Bestttttt
        except ValueError as ve: 
            return ""
        for i in range(bestIndex, len(right)): 
            if award == "":
                award = right[i]
            elif right[i] == 'for' or right[i] == 'at':
                return award
            else:
                award = award + ' ' + right[i]
        award = award.lstrip()
    return award
    

def hashNgramsKai(dff):
    FINAL_NGRAMS = []
    NGRAMS_DICT = {}
    for i in range(len(dff)):

        j = findAwards(dff['text'].iloc[i])
        if j == "":
            continue
        if j in NGRAMS_DICT:
            NGRAMS_DICT[j] += 1
        else:
            NGRAMS_DICT[j] = 1
    cd = sorted(NGRAMS_DICT.items(),key=lambda x: (x[1], len(x[0])),reverse=True)
    return cd



def CUTOFF(tu, num):
    removes = []
    for i in tu:
        if (i[1] < num):
            removes.append(i)
    for re in removes:
        tu.remove(re)
    return tu



def substringfilter(dic):
    keys = list(dic.keys())
    numKeys = len(keys)
    toRemove = []
    for key in range(numKeys-1):
        for key2 in range(key+1, numKeys):
            if keys[key] in keys[key2]:
                toRemove.append(keys[key])
    for removeKey in toRemove:
        if removeKey in dic:
            del dic[removeKey]
    return dic



def Convert(tup):
    return dict(tup)
    
def awardnames(year):
    if year=='2013':
        gg = pd.read_json('gg2013.json', orient='records')
    elif year=='2015':
        gg = pd.read_json('gg2015.json', orient='records')
    else:
        print("Wrong years")
        return
    
    copy = gg.copy(deep=True)  
    copy['text'] = copy['text'].apply(lambda x: removePunc(str(x)))
    test = list(copy['text'].values)
    s = list(set(test))
    df = pd.DataFrame(s, columns=['text'])
    con = ['Best', 'wins', ]
    con2 = ['Best']
    noncon = []
    df['Rows'] = df['text'].apply(lambda x: findRows(x, con, noncon))
    row = df[~df['Rows'].isnull()]
    lisTuples = hashNgramsKai(row)
    cutoff = 5
    filtered = CUTOFF(lisTuples, cutoff)
        
    ddd = Convert(filtered)

    #THIS IS THE OUTPUT FOR THE LIST OF STRINGS OF AWARD NAMES
    filterdictionary = substringfilter(ddd)
    results = list(filterdictionary.keys())[0:26]
    return results
