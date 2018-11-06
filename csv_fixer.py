#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import numpy as np
import pandas as pd
import editdistance
import re
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sparse_dot_topn.sparse_dot_topn as ct
from scipy.sparse import csr_matrix
import emoji_mapper
#import sparse_dot_topn.sparse_dot_topn as ct

def extract_emoji_labels(csv_to_fix, read_ext, write_ext):
    tweets = {}
    emoji_mappings = emoji_mapper.get_emoji_mappings(emoji_mapper.emoji_mappings_file)
    with open(csv_to_fix+read_ext, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        i = 0
        with open(csv_to_fix+write_ext, 'w', encoding='utf-8', newline='', buffering=1) as fixedcsv:
            writer = csv.writer(fixedcsv, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)

            for row in reader:
                if i == 0:
                    i += 1
                    continue
                #print(', '.join(row))
                i += 1
                row.append(set())
                counter = emoji_mapper.split_count(row[1])
                for emoji in counter:
                    try:
                        row[1] = row[1].replace(emoji, '')
                        row[-1].add(emoji_mappings[emoji])
                    except Exception as e:
                        pass
                writer.writerow(row)

def ngrams(string, n=3):
    string = re.sub(r'[,-./]|\sBD',r'', string)
    ngrams = zip(*[string[i:] for i in range(n)])
    return [''.join(ngram) for ngram in ngrams]


def show_similar_tweets_example(csv_to_fix, read_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, encoding='utf-8', delimiter=';', error_bad_lines=False, low_memory=False);
    full_texts = tweets['tweet_full_text'].head(100000)
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(3,3))
    tf_idf_matrix = vectorizer.fit_transform(full_texts)

    t1 = time.time()
    matches = awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), 2000, 0.3)
    print("Time after cossim: ",time.time() - t1,"s")

    matches_df = get_matches_df(matches, full_texts, top=500)
    matches_df = matches_df[matches_df['similarity'] < 0.99999] # Remove all exact matches
    pd.set_option('display.max_rows', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_columns', 3)
    print(matches_df)
    print("Time after print matches: ",time.time() - t1,"s")

def remove_similar(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, encoding='utf-8', delimiter=';', error_bad_lines=False, low_memory=False);
    full_texts = tweets['tweet_full_text']
    #Empirisch bestimmte Parameter
    vectorizer = TfidfVectorizer(analyzer='word', ngram_range=(2,2))
    tf_idf_matrix = vectorizer.fit_transform(full_texts)

    t1 = time.time()
    #Empirisch bestimmte Parameter
    matches = awesome_cossim_top(tf_idf_matrix, tf_idf_matrix.transpose(), 2000, 0.5)
    print("Time after cossim: ",time.time() - t1,"s")

    indices_to_drop = []
    non_zeroes = matches.nonzero()
    for i in range(len(non_zeroes[0])):
        if non_zeroes[0][i] < non_zeroes[1][i]:
            indices_to_drop.append(non_zeroes[1][i])
    indices_to_drop = set(indices_to_drop)

    print(indices_to_drop)
    print(len(indices_to_drop))


    tweets = tweets.drop(indices_to_drop)

    tweets.to_csv(csv_to_fix+write_ext, index=False, sep=';', quoting=csv.QUOTE_MINIMAL)
    print("Time after remove_similar: ",time.time() - t1,"s")


def awesome_cossim_top(A, B, ntop, lower_bound=0):
    # force A and B as a CSR matrix.
    # If they have already been CSR, there is no overhead
    A = A.tocsr()
    B = B.tocsr()
    M, _ = A.shape
    _, N = B.shape
 
    idx_dtype = np.int32
 
    nnz_max = M*ntop
 
    indptr = np.zeros(M+1, dtype=idx_dtype)
    indices = np.zeros(nnz_max, dtype=idx_dtype)
    data = np.zeros(nnz_max, dtype=A.dtype)

    ct.sparse_dot_topn(
        M, N, np.asarray(A.indptr, dtype=idx_dtype),
        np.asarray(A.indices, dtype=idx_dtype),
        A.data,
        np.asarray(B.indptr, dtype=idx_dtype),
        np.asarray(B.indices, dtype=idx_dtype),
        B.data,
        ntop,
        lower_bound,
        indptr, indices, data)

    return csr_matrix((data,indices,indptr),shape=(M,N))

def get_matches_df(sparse_matrix, name_vector, top=100):
    non_zeros = sparse_matrix.nonzero()
    #print(sparse_matrix)
    #print(sparse_matrix.data)
    sparserows = non_zeros[0]
    sparsecols = non_zeros[1]

    if top:
        nr_matches = top
    else:
        nr_matches = sparsecols.size

    left_side = np.empty([nr_matches], dtype=object)
    right_side = np.empty([nr_matches], dtype=object)
    similarity = np.zeros(nr_matches)

    for index in range(0, nr_matches):
        left_side[index] = name_vector[sparserows[index]]
        right_side[index] = name_vector[sparsecols[index]]
        similarity[index] = sparse_matrix.data[index]

    return pd.DataFrame({'left_side': left_side,
                          'right_side': right_side,
                           'similarity': similarity})

def remove_header_rows(csv_to_fix, read_ext, write_ext):
    with open(csv_to_fix+read_ext, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        tweets = {}
        with open(csv_to_fix+write_ext, 'w', encoding='utf-8', newline='', buffering=1) as fixedcsv:
            writer = csv.writer(fixedcsv, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row[0] == 'tweet_id':
                    #print(row)
                    continue
                tweets[row[0]] = row
            for tweet in tweets:
                writer.writerow(tweet)

def remove_linebreaks(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, encoding='utf-8', delimiter=';', error_bad_lines=False);
    tweets = tweets.replace({'\n': ' ', '\r': ' '}, regex=True)
    print(tweets.iloc[2,1])
    tweets.to_csv(csv_to_fix+write_ext, index=False, sep=';', quoting=csv.QUOTE_MINIMAL)

def remove_duplicates(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, encoding='utf-8', delimiter=';', error_bad_lines=False);
    print(tweets.shape)
    tweets = tweets.drop_duplicates(['tweet_full_text'])
    print(tweets.shape)
    tweets = tweets.drop_duplicates(['tweet_id'])
    print(tweets.shape)

    #with open(csv_to_fix+write_ext, 'w', encoding='utf-8', newline='\r\n', buffering=1) as fixedcsv:
    tweets.to_csv(csv_to_fix+write_ext, index=False, sep=';', quoting=csv.QUOTE_MINIMAL)

def sort_by_tweet_id(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, index_col=0, encoding='utf-8', delimiter=';', low_memory=False);
    tweets = tweets.sort_index(ascending=False)
    tweets.to_csv(csv_to_fix+write_ext, index=True, sep=';', encoding='utf-8', quoting=csv.QUOTE_MINIMAL, line_terminator='\r\n')

def remove_by_levenshtein(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, index_col=0, encoding='utf-8', delimiter=';');
    for i in range(len(tweets.index)):
        print(i)
        duplicates = tweets[tweets['tweet_full_text'].apply(lambda x: int(editdistance.eval(tweets.iloc[i,0], x)) / len(x) < 0.05)]
        if len(duplicates.index) > 1:
            print(duplicates)

csv_to_fix = "data/emoji_tweets/all_emoji_tweets_06_11_18"
read_initial_ext = ".csv"
fixed_line_endings_ext = "_fixed_line_endings_1.csv"
deduplicated_ext = "_deduplicated_2.csv"
sorted_ext = "_sorted_3.csv"
similar_removed_ext = "_removed_similar_4.csv"
labels_extracted_ext = "_labels_extracted_5.csv"
#remove_linebreaks(csv_to_fix, read_initial_ext, fixed_line_endings_ext)
#remove_duplicates(csv_to_fix, fixed_line_endings_ext, deduplicated_ext)
#sort_by_tweet_id(csv_to_fix, deduplicated_ext, sorted_ext)
#remove_similar(csv_to_fix, sorted_ext, similar_removed_ext)
#show_similar_tweets_example(csv_to_fix, sorted_ext)
extract_emoji_labels(csv_to_fix, similar_removed_ext, labels_extracted_ext)