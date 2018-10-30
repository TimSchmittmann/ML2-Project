#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import twitter
import time
from langdetect import detect
import csv
import config

# Create an Api instance.
api = twitter.Api(consumer_key=config.CONSUMER_KEY,
                  consumer_secret=config.CONSUMER_SECRET,
                  access_token_key=config.ACCESS_TOKEN,
                  access_token_secret=config.ACCESS_TOKEN_SECRET)

write_csv = "data/german_tweets_text_id_only_q2.csv"
maxId = 1057102141435899904
minId = False
maxLen = 0
maxLenID = 0
#tweets = []
with open(write_csv, 'a', encoding='utf-8', newline='', buffering=1) as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=['id', 'text'],
                        quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

#    fieldnames = set()
    for i in range(999999999):
        query = "lang=de&q=das%20OR%20ist%20OR%20du%20OR%20ich%20OR%20nicht%20OR%20die%20OR%20es%20OR%20und%20OR%20sie%20OR%20der%20OR%20was%20OR%20wir%20OR%20zu%20OR%20ein%20OR%20er%20OR%20in%20OR%20mir%20OR%20mit%20OR%20ja%20OR%20wie%20OR%20den%20OR%20auf%20OR%20mich%20OR%20dass%20OR%20so%20OR%20hier%20OR%20eine%20OR%20wenn%20OR%20hat%20OR%20all%20OR%20sind%20OR%20von%20OR%20dich%20OR%20war%20OR%20haben%20OR%20für%20OR%20an%20OR%20habe%20OR%20da%20OR%20nein%20OR%20bin%20OR%20noch%20OR%20dir%20OR%20uns%20OR%20sich%20OR%20nur%20-filter%3Aretweets%20-filter%3Areplies&result_type=recent&count=100"
        #query = "lang=de&q=a%20OR%20b%20OR%20c%20OR%20d%20OR%20e%20OR%20f%20OR%20g%20OR%20h%20OR%20i%20OR%20j%20OR%20k%20OR%20l%20OR%20m%20OR%20n%20OR%20o%20OR%20p%20OR%20q%20OR%20r%20OR%20s%20OR%20t%20OR%20u%20OR%20v%20OR%20w%20OR%20x%20OR%20y%20OR%20z%20-filter%3Aretweets%20-filter%3Areplies&result_type=recent&count=100"
        if maxId is not False:
            query += "&max_id="+str(maxId)
        if minId is not False:
            query += "&since_id="+str(minId)
        try:
            search = api.GetSearch(raw_query=query)
            if maxId is not False:
                # Move further into the past with each request
                maxId = search[-1].id - 1
            elif minId is not False:
                # Get the most up to date tweets per request
                minId = search[0].id + 1
            #print(max_id)
            #print([s for s in search])
            for tweetDict in search:
                tweetDict = tweetDict.AsDict()
                try:
                    if detect(tweetDict['text']) != 'de':
                        continue
                except:
                    print("This text throws and error:", tweetDict['text'])
                    continue

                tweet = {}
                '''
                for key in tweetDict:
                    if key == 'user':
                        for innerKey in tweetDict[key]:
                            tweet[key + "_" + innerKey] = tweetDict[key][innerKey]
                    elif key == 'urls' or key == 'user_mentions':
                        for j in range(len(tweetDict[key])):
                            for innerKey in tweetDict[key][j]:
                                tweet[key + "_" + str(j) + "_" + innerKey] = tweetDict[key][j][innerKey]
                    else:
                        tweet[key] = tweetDict[key]
                '''
                tweet['id'] = tweetDict['id']
                tweet['text'] = tweetDict['text']
                #print(str(tweet['id'])+": "+tweetDict['created_at'])
                writer.writerow(tweet)
            #           fieldnames.update(tweet.keys())
            #            tweets.append(tweet)
            print(i)
            time.sleep(5)
        except Exception as e:
            print(str(e))
            time.sleep(30)