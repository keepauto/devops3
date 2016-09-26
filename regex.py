# -*- encoding: utf8  -*-
import re

def readfile():
    wordlist=[]
    templist=[]
    wordcount={}
    pattern=re.compile(r'\w+')
    base=open('EnglishWord.txt','r')
    baseinfo=base.readlines()
    for i in baseinfo:
        wordlist=re.findall(pattern,i)
        for word in wordlist:
            if word not in templist:
                templist.append(word)
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    wordcount=sorted(wordcount.iteritems(), key=lambda d:d[1], reverse=True)
    
    for word in wordcount:
        print word

if __name__== "__main__":
    readfile()
