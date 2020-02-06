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
import scipy
from array import *
import pandas as pd
import numpy as np
import gensim 
from gensim.models import Word2Vec
from pyemd import emd
from gensim.similarities import WmdSimilarity

import spacy
nlp = spacy.load("en_core_web_lg")

import wmd
nlp2 = spacy.load('en_core_web_lg', create_pipeline=wmd.WMD.create_spacy_pipeline)
nlp2.add_pipe(wmd.WMD.SpacySimilarityHook(nlp2), last=True)

#Specifying the corpus that will be used
#corpus = pd.read_csv('/Users/Cylita/Desktop/insight-ds-project_news-link/data/cleaned/Final_Cleaned_Corpus.txt')
#Corpus for validation


#####Setting key variables for flask app based on corpus
#Separating out fully cleaned stories
#stories = corpus['cleaned_text']
#Calculating length of stories and storing in a list
#story_length = []

#for story in stories:
   # forcount = len(story.split())
    #story_length.append(forcount)

#Calculating the value for the 90th percentile
#length_array = np.array(story_length)
#percentile_90 = np.percentile(length_array, 90) # return 90th percentile
#percentile_85 = np.percentile(length_array, 85) #return the 85th percentile

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
    topX = sorted_news.iloc[0:NumLinks, [title,mainurl, sim]]
    #Function returns the top set of links for a story of interest
    return topX

###########Func3
# Following function uses similarity scores to compute similarity metrics for top specified stores

def StoryMatch_Val (SimScores, originalDF, NumLinks = 10):
    #Appending similarity scores to new dataframe
    originalDF['sim_scores'] = SimScores
    
    #Sorting dataframe in ascending order based on similarity scores
    sorted_news = originalDF.sort_values(by=['sim_scores'], ascending = False)
    
    #Getting index for story title column
    title = originalDF.columns.get_loc("title")
    
    #Getting index for story url
    mainurl = originalDF.columns.get_loc("mainurl")
    
    #Getting url for similar story
    sim1url = originalDF.columns.get_loc("sim1")

    #Getting index for similarity scores
    sim = originalDF.columns.get_loc("sim_scores")
    
    
    #Isolating the specificed number of links (10 default)
    topX = sorted_news.iloc[0:NumLinks, [title,mainurl, sim1url, sim]]
    #Function returns the top set of links for a story of interest
    return topX


###########Func4
# Following function will be called to pull similarity metrics 
def Top10(TestScores, TestStory):
    Top10 = TestScores.iloc[0:9]
    InTen = Top10['sim1'].isin(pd.Series(TestStory['sim1']))
    
    if True in InTen:
        output = 1
    else:
        output = 0
    
    return output

###########Func5
# Following function will be called to pull similarity metrics 
def FindSimScore (TestScores, TestStory):
    findsim = TestScores.loc[TestScores['mainurl'] == TestStory['sim1']]
    output = findsim['sim_scores'].iloc[0]
    return output

###########Func6
# Following function will be called to pull similarity metrics 
def FindSimScoreWMD (TestScores, TestStory):
    findsim = TestScores.loc[TestScores['mainurl'] == TestStory['sim1']]
    output = findsim['wmd_scores'].iloc[0]
    return output


###########Func6
#Following function will be called to compute word embeddings for just the corpus

def GloveEmbeds (corpus):

    doc_vector = []

    #Calculates the Glove Embeddings using spacy
    for doc in corpus['cleaned_text']:
        embeddings = nlp(doc)
        doc_vector.append(embeddings)
    
    #Function retruns list of corpus word embeddings
    return doc_vector

def GloVeCosine (querydoc, corpus_embeddings):

    #Calculates word embeddings for the story of interest
    query = nlp(querydoc)

    #list to hold similarity scores
    sim_scores = []

    #Loop to calculate query story similarity to all other stories in the corpus
    for doc in corpus_embeddings:
        score = query.similarity(doc)
        sim_scores.append(score)

    #retruning similairty scores
    return sim_scores

def WMDEmbeds (corpus):

    doc_vectorWMD = [ ]

    #Calculates the GloVe Embeddings using the WMD pipeline in Spacy
    for doc in corpus['cleaned_text']:
    WMDembbeddings = nlp2(doc)
    doc_vectorWMD.append(WMDembbeddings)

    return doc_vectorWMD

def GloVeWMD(corpus_embeddings, querydoc)
    
    #Calculates word embeddings for the story of interest
    query = nlp2(querydoc)

    #list to hold similarity scores
    sim_scores = []

    #Loop to calculate query story similarity to all other stories in the corpus
    for doc in corpus_embeddings:
        score = query.similarity(doc)
        sim_scores.append(score)

    #retruning similairty scores
    return sim_scores


###########Func7
#Use the WMD scores to order original dataframe

def EmbeddingMatch (scores, originalDF, NumLinks=10):
    #Appending similarity scores to new dataframe
    originalDF['wmd_scores'] = scores
    
    #Sorting dataframe in ascending order based on similarity scores
    sorted_news = originalDF.sort_values(by=['wmd_scores'], ascending = True)
    
    #Getting index for story title column
    title = originalDF.columns.get_loc("title")
    
    #Getting index for story url
    mainurl = originalDF.columns.get_loc("mainurl")
    
    #Getting url for similar story
    sim1url = originalDF.columns.get_loc("sim1")

    #Getting index for similarity scores
    sim = originalDF.columns.get_loc("wmd_scores")
    
    
    #Isolating the specificed number of links (10 default)
    topX = sorted_news.iloc[0:NumLinks, [title,mainurl, sim1url, sim]]
    
    #Function returns the top set of links for a story of interest
    return topX













