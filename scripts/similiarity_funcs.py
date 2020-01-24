#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 17:17:17 2020

@author: Cylita
"""

'''
Following script contains functions that will be used to compute similarity 
metricies for an inputed group of articles against the existing copora of text

'''
#Packages and functions
from nltk.tokenize import word_tokenize
import gensim
import spacy
import nltk
from array import *

#####Func 1
#Processing the corpus for comparison and generating similarity indicies for a body of text

def SimCorpCreate (corpora, directory, querydoc):
    #Creating empty list to store the tokenized words for comparison from docs
    token_comp = []
    
    for doc in corpora:
        tokens = word_tokenize(doc)
        token_comp.append(tokens)
    
    #Creating a dictionary
    dictionary = gensim.corpora.Dictionary(token_comp)
    
    #Creating corpus of words usign the dictionary
    corpus = [dictionary.doc2bow(doc) for doc in token_comp]
    
    #Caclulating frequency–inverse document frequency
    tf_idf = gensim.models.TfidfModel(corpus)
    
    #Building similiarity index to be saved wherever this script is
    sims = gensim.similarities.Similarity(directory,tf_idf[corpus],
                                        num_features=len(dictionary))
    
    #Tokenizing query text and creating a dictionary
    querytokens = word_tokenize(querydoc)
    query_doc_bow = dictionary.doc2bow(querytokens)
    
    # perform a similarity query against the corpus
    query_doc_tf_idf = tf_idf[query_doc_bow]
    
    #Attatch to list for outputs
    sim_scores = sims[query_doc_tf_idf]

    #Turn array into a list
    sim_out = sim_scores.tolist()
    
    return sim_out

###########Func2
# Following function uses similarity scores to compute similarity metrics for top specified stores

def StoryMatch (SimScores, originalDF, NumLinks = 10):
    #Appending similarity scores to new dataframe
    originalDF['sim_scores'] = SimScores
    
    #Sorting dataframe in ascending order based on similarity scores
    sorted_news = originalDF.sort_values(by=['sim_scores'], ascending = False)
    
    #Getting index for story title column
    title = originalDF.columns.get_loc("title")
    
    #Getting index for story url
    mainurl = originalDF.columns.get_loc("mainurl")

    #Getting index for similarity scores
    sim = originalDF.columns.get_loc("sim_scores")
    
    #Isolating the specificed number of links (10 default)
    topX = sorted_news.iloc[1:NumLinks, [title,mainurl, sim]]
    #Function returns the top set of links for a story of interest
    return topX
