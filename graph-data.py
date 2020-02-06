#! /usr/bin/python3
#4 Submitted by Adrian Salinas
import sys
import requests
from textblob import TextBlob
import io
import pandas as pd
import re
import matplotlib.pyplot as plt


print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of an html file to extract the text from!")
    sys.exit()
else:
    text = open(sys.argv[1],"r")

txt = text.read()
print("Reading in %s " % str(sys.argv[1]))
txt = txt.replace('\n', ' ').replace('\r', ' ')
txt = txt.replace('. ', '\n')

f = io.StringIO(txt)
numbered = f.readlines()

rows_list = []
i=1
for h in numbered:
    new_row = {'line':i, 'text':h.strip()}
    rows_list.append(new_row)
    i+=1


    def get_polarity(text):
        try:
            return TextBlob(text).sentiment.polarity
        except Exception:
            print("An exception occurred.")
            return 'n/a'

    def get_subjectivity(text):
        try:
            return TextBlob(text).sentiment.subjectivity
        except Exception:
            print("An exception occurred.")
            return 'n/a'

def is_pos(pol):
    if (pol > 0):
        return 1
    else:
        return 0

def is_neg(pol):
    if (pol < 0):
        return 1
    else:
        return 0

df = pd.DataFrame(rows_list,columns=['line','text'])

df['polarity'] = df['text'].apply(get_polarity)
df['subjectivity'] = df['text'].apply(get_subjectivity)


df['polsum'] = df['polarity'].cumsum()
df['pos'] = df['polarity'].apply(is_pos)
df['neg'] = df['polarity'].apply(is_neg)
df['possum'] = df['pos'].cumsum()
df['negsum'] = df['neg'].cumsum()


df2 = df[['line', 'polsum','possum', 'negsum']]


plottitle = "Adrian Salinas \n" + str(sys.argv[1])
print("This has no chapter number")






fig, ax = plt.subplots(facecolor='grey')
ax.set_facecolor('#a6a6a6')
ax.set_title(plottitle, color='black')
ax.set_xlabel('Line Number', color='black')
ax.set_ylabel('Occurences', color='black')
ax.plot(df2['line'], df2['polsum'], '#808080', label='Overall Polarity')
ax.plot(df2['line'], df2['possum'], 'xkcd:darkgreen', label='Positive statement')
ax.plot(df2['line'], df2['negsum'], 'xkcd:crimson', linestyle='--', label='Negative statement')
ax.tick_params(labelcolor ='grey')
plt.legend()




pngname = str(sys.argv[1]).split('.')[0] + "_pos-neg.png"

plt.savefig(pngname)
print("The png %s has been written" % pngname)
