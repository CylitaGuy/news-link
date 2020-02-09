#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 22:06:52 2020

@author: Cylita
"""

'''

This file is run to create the metrics to be used to validate the approach using GloVe embeddings
and Word Mover's Distance (see Data Viz notebook).

'''

#required functions and py files
import pandas as pd
import sys

#specifying local system path for remaining functions files
sys.path.insert(1, '/Users/Cylita/Desktop/insight-ds-project_news-link/scripts')

#self written functions and scripts that will be needed
import similiarity_funcs as SIM

#Reading in the data
val_corpus = pd.read_csv("/Users/Cylita/Desktop/insight-ds-project_news-link/data/cleaned/Val_Corpus.csv")

#Removing duplciate stories that have been included in the corpus
unique_val = val_corpus.drop_duplicates(subset=['mainurl'])

#Creating a dataframe that has all of the rows for analysis separated
#Dataframe keeps the original indicies for rows
news_validation = unique_val[~pd.isna(unique_val['sim1'])]

#Creating a subset of stories to test
news_test = news_validation.iloc[0:2,]


#Setting up three empty lists to store similarity scores
my1score = []
jourscore = []
top10orNaw = []


#looping the following over ever row in my data frame
for index, row in news_validation.iterrows():
    #Using the row index to separate out test story and remaining stories for text corpus
    teststory = news_validation.loc[index,]
    corpus = unique_val.drop([index], axis=0)
    
    #Creating corpus from above GloVe embeddings
    embeds = SIM.WMDEmbeds(corpus = corpus)
    
    #Computing similarity scores for given dataframe - here word mover's distance
    scores = SIM.GloVeWMD(corpus_embeddings = embeds, querydoc = teststory['cleaned_text'])
    
    #Appending similarity scores to original
    valscores = SIM.EmbeddingMatch (scores = scores, originalDF = corpus, NumLinks=len(corpus))

    #Adding value of most similar story to the list
    my1score.append(valscores['wmd_scores'].iloc[0])
    
    #Using function to determined if similar link is in my top 10
    top = SIM.Top10(TestScores = valscores, TestStory = teststory)
    top10orNaw.append(top)
    
    #Finding similarity score for the link directly inserted by the journalists
    try:
        journal = SIM.FindSimScoreWMD(TestScores = valscores, TestStory= teststory)
    except (IndexError):
        journal = "NA"
        
    jourscore.append(journal)


#Combine all output together into one file
output_validation = {'MyModel':my1score, "JournalScore" : jourscore, "Top10": top10orNaw}

#Creating a dataframe and saving as csv. 
val_data = pd.DataFrame(output_validation)
val_data.to_csv("validation_metrics_wmd.csv")
