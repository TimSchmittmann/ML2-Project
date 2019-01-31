from flask import Flask
from joblib import load
import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
import bottleneck as bn
import nltk
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from flask import request
import json
 
from nltk.corpus import stopwords 
stopwords_german = stopwords.words('german')
 
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer('german')
 
from nltk.tokenize import TweetTokenizer
 
# Happy Emoticons
emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
# Sad Emoticons
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
# all emoticons (happy + sad)
emoticons = emoticons_happy.union(emoticons_sad)
 
def clean_tweets(tweet):
    # remove stock market tickers like $GE
    tweet = re.sub(r'\$\w*', '', tweet)
 
    # remove old style retweet text "RT"
    tweet = re.sub(r'^RT[\s]+', '', tweet)
 
    # remove hyperlinks
    tweet = re.sub(r'https?:\/\/[^\s]*', '', tweet)
    
    # remove hashtags
    # only removing the hash # sign from the word
    tweet = re.sub(r'#', '', tweet)
    
    # replace years with 'ayearzzz'-Token
    tweet = re.sub(r'([1-2][0-9]{3})', r'ayearzzz', tweet)
    
    # replace numbers with 'anumberzzz'-Token, only numbers outside of words
    tweet = re.sub(r'(?<![0-9a-zA-Z])[0-9]+(?![0-9a-zA-Z])', r'anumberzzz', tweet)
 
    # tokenize tweets
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)
 
    tweets_clean = []    
    for word in tweet_tokens:
        if (word not in stopwords_german and # remove stopwords
              word not in emoticons and # remove emoticons
                word not in string.punctuation): # remove punctuation
            #tweets_clean.append(word)
            stem_word = stemmer.stem(word) # stemming word
            tweets_clean.append(stem_word)
    tweets_clean=" ".join(tweets_clean)
    
    # remove numbers that were pulled out of words by tokenizer
    tweets_clean = re.sub(r'(?<![0-9a-zA-Z])[0-9]+(?![0-9a-zA-Z])', r'', tweets_clean)
    
    return tweets_clean
	
def sparse_to_emoji_array(sparse, classes):
    emoji_labels = np.empty(sparse.shape[0], dtype=object)
    nonzero_rows = sparse.nonzero()[0]
    nonzero_cols = sparse.nonzero()[1]
    for i in range(len(nonzero_rows)):
        if emoji_labels[nonzero_rows[i]] is None:
            emoji_labels[nonzero_rows[i]] = []
        emoji_labels[nonzero_rows[i]].append(classes[nonzero_cols[i]])
    return emoji_labels
	
clf = load('grid_classifier_chain_multinomial_nb_reduced_2_handpicked_labels.joblib') 
vectorizer = load('vectorizer_reduced_2_handpicked_labels.joblib')
mlb = load('mlb_reduced_2_handpicked_labels.joblib')
app = Flask(__name__)

@app.route('/get-predictions',methods=['POST'])
def get_predictions():
	app.logger.error(request.data)
	msg = request.form['msg']
	msg = vectorizer.transform([clean_tweets(msg)]) 
	predicted = clf.predict(msg)
	predict_proba = clf.predict_proba(msg)

	f = lambda arr: bn.argpartition(arr, arr.size-1)[-1:]
	single_pred = [f(x) for x in predict_proba.A]
	predicted = predicted.A
	for i in range(len(predicted)):
		if not predicted[i].any():
			predicted[i][single_pred[i]] = 1

	predicted_labels = sparse_to_emoji_array(predicted, mlb.classes_)
	return json.dumps(predicted_labels[0])
	