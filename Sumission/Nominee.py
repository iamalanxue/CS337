#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import operator
import string
import nltk 
from nltk.tag import pos_tag
import json
from collections import Counter
from nltk.util import ngrams


pd.set_option('display.width', 10000)


# In[2]:


stopword = nltk.corpus.stopwords.words('english')
#stopword.extend(['best', 'picture', 'musical', 'Best', 'Picture', 'Musical', 'Comedy', 'comedy', 'RT'])





def removePunc(x):
#     new_string = x.translate(str.maketrans('', '', string.punctuation))
    x = re.sub(r'[@#]\w+', '', x) #taking out hashtags and @ 
    x = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', x) #taking out links 
    x = re.sub(r'[!?\.,\'\":()]+', '', x) #taking out punctuation i.e ? ! . ' : ( ) and " 
    x = re.sub(r'(RT|rt) ', '', x) #taking out the initial "RT "
    x= re.sub(r'(g|G)olden (g|G)lobes', '', x)
    return x.strip()




def getMovieNom(winner,tweets):
        f=open('MovieDatabase.txt',encoding='utf-16')
        moviedic={}
        tweets = tweets.str.lower()
        tweets = tweets.apply(lambda x: removePunc(str(x)))
        for i in f.read().split('\n'):
            try:
                k=i
                if k:
                    moviedic[k.lower()]=1
            except:
                continue
        f.close()
        count=0
        movies = {}
        movies[winner]=1
        for tweet in tweets:
            if winner in tweet:
                token = nltk.word_tokenize(tweet)
                bigrams = ngrams(token,2)
                trigrams= ngrams(token,3)
                GG=Counter(bigrams)+Counter(trigrams)+Counter(token)
                for i in GG.most_common(50):
                    if len(i[0])>3:
                        xx=i[0]
                    else:
                        xx=' '.join(k for k in i[0]).lower()
                    if 'the' in xx and len(xx.split())<3:
                        continue
                    if xx in moviedic.keys():
                        movies[xx]=1
                        count+=1
            if count>10:
                break
        a=list(movies.keys())[0:6]
        if winner in a:
            a.remove(winner)
        return a

def Achive_names(tweet,winner,threshhold):
    blacklist=['golden','best','globe','motion','actor','actress','hero','picture','drama']
    count=0
    names={}
    nltk_results = nltk.ne_chunk(pos_tag(nltk.word_tokenize(tweet)))
    for chunk in nltk_results:
        if type(chunk) == nltk.tree.Tree:
            if chunk.label() == 'PERSON':
                l=[]
                for c in chunk[0:4]:
                    if c[0].lower() in blacklist:
                        break
                    else:
                        l.append(c[0])
                temp = ' '.join(l)
                if len(temp.split())==2:
                    if temp not in names:
                        count+=1
                        names[temp.lower()]=1
                    else:
                        names[temp.lower()]+=1
    if count>=threshhold:
        return names
    return []


def getNominee(award,winner,tweets):
        res=[]
        if 'actor'in award or 'actress'in award or 'performance' in award or 'director'in award or'award'in award:
            for tweet in tweets:
                if winner in tweet.lower():
                    result=Achive_names(tweet,winner,5)
                    if result:
                        candidate=list(result.keys())
                        if winner in candidate:
                            candidate.remove(winner)
                            res.extend(candidate)
            return list(set(res))
        else:
            return getMovieNom(winner,tweets)
        


#getNominee("best original score - motion picture","life of pi",copy['text'])

def Nominees(year):
    if year=='2013':
        gg = pd.read_json('gg2013.json', orient='records')
        winner_list= {'cecil b. demille award': 'jodie foster', 'best motion picture - drama': 'argo', 
                    'best performance by an actress in a motion picture - drama': 'jessica chastain', 
                    'best performance by an actor in a motion picture - drama': 'daniel day-lewis', 
                    'best motion picture - comedy or musical': 'les miserables', 
                    'best performance by an actress in a motion picture - comedy or musical': 'jennifer lawrence', 
                    'best performance by an actor in a motion picture - comedy or musical': 'hugh jackman', 
                    'best animated feature film': 'brave', 'best foreign language film': 'amour', 
                    'best performance by an actress in a supporting role in a motion picture': 'anne hathaway', 
                    'best performance by an actor in a supporting role in a motion picture': 'christoph waltz', 
                    'best director - motion picture': 'ben affleck', 'best screenplay - motion picture': 'django unchained', 
                    'best original score - motion picture': 'life of pi', 'best original song - motion picture': 'skyfall', 
                    'best television series - drama': 'homeland', 'best performance by an actress in a television series - drama': 'claire danes', 
                    'best performance by an actor in a television series - drama': 'damian lewis', 'best television series - comedy or musical': 'girls', 
                    'best performance by an actress in a television series - comedy or musical': 'lena dunham', 
                    'best performance by an actor in a television series - comedy or musical': 'don cheadle', 
                    'best mini-series or motion picture made for television': 'game change', 'best performance by an actress in a mini-series or motion picture made for television': 'julianne moore', 
                    'best performance by an actor in a mini-series or motion picture made for television': 'kevin costner', 
                    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'maggie smith', 
                    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'ed harris'}
    elif year=='2015':
        gg = pd.read_json('gg2015.json', orient='records')
        winner_list={'cecil b. demille award': 'george clooney', 'best motion picture - drama': 'boyhood', 
                    'best performance by an actress in a motion picture - drama': 'julianne moore', 
                    'best performance by an actor in a motion picture - drama': 'eddie redmayne', 
                    'best motion picture - comedy or musical': 'the grand budapest hotel', 
                    'best performance by an actress in a motion picture - comedy or musical': 'amy adams', 
                    'best performance by an actor in a motion picture - comedy or musical': 'michael keaton', 
                    'best animated feature film': 'how to train your dragon 2', 'best foreign language film': 'leviathan', 
                    'best performance by an actress in a supporting role in a motion picture': 'patricia arquette', 
                    'best performance by an actor in a supporting role in a motion picture': 'j.k. simmons', 
                    'best director - motion picture': 'richard linklater', 'best screenplay - motion picture': 'birdman', 
                    'best original score - motion picture': 'the theory of everything', 'best original song - motion picture': 'selma', 
                    'best television series - drama': 'the affair', 'best performance by an actress in a television series - drama': 'ruth wilson', 
                    'best performance by an actor in a television series - drama': 'kevin spacey', 'best television series - comedy or musical': 'transparent', 
                    'best performance by an actress in a television series - comedy or musical': 'gina rodriguez', 
                    'best performance by an actor in a television series - comedy or musical': 'jeffrey tambor', 
                    'best mini-series or motion picture made for television': 'fargo', 
                    'best performance by an actress in a mini-series or motion picture made for television': 'maggie gyllenhaal', 
                    'best performance by an actor in a mini-series or motion picture made for television': 'billy bob thornton', 
                    'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'joanne froggatt', 
                    'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'matt bomer'}
    else:
        print("Wrong years")
        return
    copy = gg.copy(deep=True)
    result={}
    for key in winner_list:
        nominee=getNominee(key,winner_list[key],copy['text'])
        result[key]=nominee
        
    return result 

