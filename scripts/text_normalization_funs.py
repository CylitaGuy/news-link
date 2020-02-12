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

#Loading small spacy english language model (contains no vectors)
nlp = spacy.load('en')

#Importing custom disctionary of english language common contractions 
CONTRACTION_MAP = {
"ain't": "is not",
"aren't": "are not",
"can't": "cannot",
"can't've": "cannot have",
"'cause": "because",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hadn't've": "had not have",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'd've": "he would have",
"he'll": "he will",
"he'll've": "he he will have",
"he's": "he is",
"how'd": "how did",
"how'd'y": "how do you",
"how'll": "how will",
"how's": "how is",
"I'd": "I would",
"I'd've": "I would have",
"I'll": "I will",
"I'll've": "I will have",
"I'm": "I am",
"I've": "I have",
"i'd": "i would",
"i'd've": "i would have",
"i'll": "i will",
"i'll've": "i will have",
"i'm": "i am",
"i've": "i have",
"isn't": "is not",
"it'd": "it would",
"it'd've": "it would have",
"it'll": "it will",
"it'll've": "it will have",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"mayn't": "may not",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"so's": "so as",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what'll've": "what will have",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who'll've": "who will have",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you'll've": "you will have",
"you're": "you are",
"you've": "you have"
}


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