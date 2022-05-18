#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re
import operator
import string
import nltk 
from nltk.tag import pos_tag
pd.set_option('display.width', 10000)


# In[2]:


stopword = nltk.corpus.stopwords.words('english')
stopword.extend(['best', 'picture', 'musical', 'Best', 'Picture', 'Musical', 'Comedy', 'comedy', 'RT'])



def removePunc(x):
#     new_string = x.translate(str.maketrans('', '', string.punctuation))
    x = re.sub(r'[@#]\w+', '', x) #taking out hashtags and @ 
    x = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', x) #taking out links 
    x = re.sub(r'[!?\.,\'\":()]+', '', x) #taking out punctuation i.e ? ! . ' : ( ) and " 
    x = re.sub(r'(RT|rt) ', '', x) #taking out the initial "RT "
    x= re.sub(r'(g|G)olden (g|G)lobes', '', x)
    return x.strip()



def nGram(text):
    test = text
    firstsplit = test.split(' wins ', 1)
    if len(firstsplit) > 1:
        left = firstsplit[0].split(' ')
        left.reverse()
        new_list = []
        x = ""
        for i in left:
            if(i == ""):
                new_list.append(x) #HACKS
                continue
            x =  i + " " + x 
            new_list.append(x)
        new_list = [x.rstrip() for x in new_list]
    else:
        new_list = []
    return new_list


def hashNgrams(dff):
    FINAL_NGRAMS = []
    NGRAMS_DICT = {}
    for i in range(len(dff)):
        l = nGram(dff['text'].iloc[i])
        for j in l:
            if j in NGRAMS_DICT:
                NGRAMS_DICT[j] += 1
            else:
                NGRAMS_DICT[j] = 1
    cd = sorted(NGRAMS_DICT.items(),key=lambda x: (x[1], len(x[0])),reverse=True)
    return cd[0][0]



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



ALLAWARDS = [['best', 'picture', 'drama'], ['actor', 'actress'],
['best', 'picture', 'musical', 'comedy'], ['actor', 'actress'],
['best', 'picture', 'drama', 'actress'], ['actor'],
['best', 'picture', 'drama', 'actor'], ['actress'],
['best', 'picture', 'musical', 'comedy', 'actress'], ['actor'],
['best', 'picture', 'musical', 'comedy', 'actor'], ['actress'],
['best', 'picture', 'supporting', 'actress'], ['actor'],
['best', 'picture', 'supporting', 'actor'], ['actress'],
['best', 'picture', 'director'], [],
['best', 'picture', 'screenplay'], [],
['best', 'picture', 'animated'], [],
['best', 'foreign', 'language'], [],
['best', 'picture', 'score'], [],
['best', 'picture', 'song'],[],
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


# In[11]:


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


# In[12]:


def findAllWinners(matrix):
    winners = []
    for i in range(0, len(matrix), 2):
        con = matrix[i]
        noncon = matrix[i+1]
        df['Rows'] = df['text'].apply(lambda x: findRows(x, con, noncon)) #Problems here  Df is defined outside of the function
        ccc = df[~df['Rows'].isnull()]
        winner = hashNgrams(ccc)
        print(winner)
        winners.append(winner)
    return winners



def makeDict(winners, awards):
    awardNames = {}
    for i in range(len(winners)):
        awardNames[awards[i]] = winners[i]
    return awardNames


def award_winners(year):
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

    test = list(copy['text'].values)
    s = list(set(test))
    df = pd.DataFrame(s, columns=['text'])

    con = ['best', 'tv', 'drama', 'actor']
    noncon = ['actress']
    df['Rows'] = df['text'].apply(lambda x: findRows(x, con, noncon))
    df.head(20)

    ccc = df[~df['Rows'].isnull()]
    hashNgrams(ccc)
    win = findAllWinners(ALLAWARDS)
    #THIS IS THE OUTPUT FOR AWARD WINNERS WHICH IS A DICTIONARY KEYS: AWARD NAMES || VALUE: AWARD WINNERS
    GGWINNERS = makeDict(win, awardNames)
    return GGWINNERS

print(award_winners('2013'))