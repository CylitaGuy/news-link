#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:21:25 2020

@author: Cylita
"""

'''

Following file contains functions that will be used to normalize and clean text.

'''

#Import needed packages
import spacy
import re
import unicodedata
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
#Importing custom disctionary of english language common contractions 
from contractions import CONTRACTION_MAP
#Loading small spacy english language model (contains no vectors)
nlp = spacy.load('en')

###########
#Function 1: Converting all text to lowercase 
def lowercase_text(text):
    text_lower = text.lower()
    return text_lower

###########
#Function 2: Removing all numbers from text 
    
def nonums(text):
    pattern = '[0-9]'
    #substituting regular expressions with numbers with a space
    output = re.sub(pattern,'', text)
    return output

###########
#Function 3: Removing accented charecters
    
def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

###########
#Function 4: Expanding common english contractions

def expand_contractions(text, contraction_mapping=CONTRACTION_MAP):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text

###########
#Function 5: Remove punctuation and other special charecters
    
def special2(text):
    modified_string = re.sub(r'[^a-zA-Z0-9_\s]+', '', text)
    output = modified_string.replace('_', '')
    return output

###########
#Function 6: Remove stopwords

def nostopwords(text):
    #Using nlkt library to set common english stopwords
    stop_words = set(stopwords.words('english'))
    #Creating word tokens from body of text
    word_tokens = word_tokenize(text)
    #Filitering tokens for stopwords
    filtered_tokens = [token for token in word_tokens if token not in stop_words]
    #Filtering text
    filtered_text = ' '.join(filtered_tokens) 
    return filtered_text

###########
#Function 7:Lemmetize text
    
def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([word.lemma_ if word.lemma_ != '-PRON-' else word.text for word in text])
    return text

###########
#Function 8: Text Normalizer
#Combines all other functons to clean text

def normalize_NewsText(corpus):
    
    normalized_corpus = []
    
    # normalize each document in the corpus
    for doc in corpus:
        #remove capital letters
        a = lowercase_text(doc)
        #removing numbers
        b = nonums(a)
        #removing accented characters
        c = remove_accented_chars(b)
        #expanding all contractions
        d = expand_contractions(c)
        #removing special characters and punctuations
        e = special2(d)
        #removing stop words
        f = nostopwords(e)
        #lemmatizing text
        g = lemmatize_text(f)

        #Appending new normalized text to the list of interest
        normalized_corpus.append(g)
        
    return normalized_corpus
        
#####Func 9: Taking first 30% of cleaned text
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