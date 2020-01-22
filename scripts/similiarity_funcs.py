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

#####Func 1
#Function meant to isolate the first 30% of the cleaned story text (or sentances) for analysis

def Clean30 (text):
    #Split the text into individual words or sentances
    text_split = text.split(" ")
    #Take the first 30% of words included in the text body
    First30 = text_split[0:len(text_split)//3]
    #Join back the first 30
    First30_str = " ".join(First30)
    #Return the joined text
    return First30_str

#####Func 1
#Function for creating the corpus of text that another story will be compared to

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
    
    #Creating a list to story query cosine similarity scores
    cosine_simscore = []
    
    # perform a similarity query against the corpus
    query_doc_tf_idf = tf_idf[query_doc_bow]
    
    #Attatch to list for outputs
    cosine_simscore.append(sims[query_doc_tf_idf])
    
    return cosine_simscore

