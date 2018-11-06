import emoji
import regex
import csv
import time
import pandas as pd

tweet_file = "data/emoji_tweets/all_emoji_tweets_06_11_18_removed_similar_4.csv"
emoji_mappings_file = "data/emoji_mapping.csv"

def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)

    return emoji_list

def get_emoji_mappings(emoji_mappings_file):
    emoji_mappings = {}
    with open(emoji_mappings_file, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            for emoji in row[0].split(','):
                try:
                    if(int(row[1]) > 0):
                        emoji_mappings[emoji] = row[0]
                except:
                    emoji_mappings[emoji] = row[1]
    return emoji_mappings

def map_emojis_in_tweets(tweet_file, emoji_mappings):
    tweets_labels = {}
    with open(tweet_file, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 0
        for row in reader:
            if i == 0:
                i += 1
                continue
            #print(', '.join(row))
            i += 1
            tweets_labels[row[0]] = set()
            counter = split_count(row[1])
            for emoji in counter:
                try:
                    tweets_labels[row[0]].add(emoji_mappings[emoji])
                except Exception as e:
                    pass
                    #print(str(e))
                    #print("No mapping for emoji: ",emoji)

    return tweets_labels

if __name__ == '__main__':
    t1 = time.time()
    emoji_mappings = get_emoji_mappings(emoji_mappings_file)
    tweets = map_emojis_in_tweets(tweet_file, emoji_mappings)
    #print(tweets)
    print("Extraction takes ",time.time()-t1,"s")
