import pandas as pd
import re
import operator
import string
import nltk 
import sys
from nltk.tag import pos_tag
def removePunc(x):
  x = re.sub(r'[@#]\w+', '', x) #taking out hashtags and @ 
  x = re.sub(r'(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)', '', x) #taking out links 
  x = re.sub(r'[!?\.,\'\"]+', '', x) #taking out punctuation i.e ? ! . ' and " 
  return x.strip()

def findProperNouns(sen):
    tagged_sent = pos_tag(sen.split())
    propernouns = [word for word,pos in tagged_sent if pos == 'NNP']
    return propernouns

def GETHOSTNAMES(year):
  gg = pd.read_json('gg2013.json', orient='records')
  gg1 = pd.read_json('gg2015.json', orient='records')
  copy = gg.copy(deep=True)
  if year == '2015':
    copy = gg1.copy(deep=True)
  copy['text'] = copy['text'].apply(lambda x: removePunc(str(x)))
  test = list(copy['text'].values)
  s = list(set(test))
  df = pd.DataFrame(s, columns=['text'])
  df = df.loc[df['text'].str.contains('host')]
  df['ProperNouns'] = df['text'].apply(lambda x: findProperNouns(x))
  NGRAMS_DICT = {}
  for i in range(len(df)):
    PN = df['ProperNouns'].iloc[i]
    if len(PN) % 2 == 0: 
      for j in range(0, len(PN), 2):
        name = PN[j] + ' ' + PN[j+1]
        if name in NGRAMS_DICT:
          NGRAMS_DICT[name] += 1
        else:
          NGRAMS_DICT[name] = 1
  cd = sorted(NGRAMS_DICT.items(),key=operator.itemgetter(1),reverse=True)
  top3 = [i[0] for i in cd[0:3]]
  return top3

user_in = sys.argv[1]
host = GETHOSTNAMES(user_in)
print(host)
