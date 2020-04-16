#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 21:26:59 2017

@author: alexanderhoward
"""
#python2.6
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re

def calctime(a):
    return time.time()-a

pos=0
neg=0
comp=0
count=0

initime=time.time()
plt.ion()

consumer_key = 'ObUnSmPdtMdf7lnTAyYOOAlY5'
consumer_secret = 'QBHHFrW1rXAFviu8CllUoIZvvlUu3bXUtNpxTQ1ddw7qpUDv5L'

access_token = '741124847414169600-8L2m08Hlase1qyWV8xcs1Ndlo8Myxep'
access_token_secret = '83gTXg7vFdWSy5raF14rpAoAm6YJR6Hp36qiqYmaEAE6v'

class listener(StreamListener):
    
    def on_data(self,data):
        global initime
        t=int(calctime(initime))
        all_data=json.loads(data)
        tweet=all_data["text"].encode("utf-8")
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet))
        blob=TextBlob(tweet.strip())
        
        global pos
        global neg
        global comp
        global count
        
        count += 1
        senti=0
        for sen in blob.sentences:
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                pos=pos+sen.sentiment.polarity
            else:
                neg=neg+sen.sentiment.polarity
        comp=comp+senti
        print count
        print tweet.strip()
        print senti
        print t
        print str(pos) + " " + str(neg) + " " + str(comp)
        
        plt.axis([ 0, 70, -20, 20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([t],[pos],'go',[t] ,[neg],'ro',[t],[comp],'bo')
        plt.show()
        plt.pause(0.0001)
        if count==200:
            return False
        else:
            return True
            
    def on_error(self,status):
        print status
        

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream= Stream(auth, listener(count))
#twitterStream.filter(track=["Donald Trump"])

def main(entity,twitterSteam):
    twitterStream.filter(track=[ entity])

main("Donald Trump",twitterStream)







