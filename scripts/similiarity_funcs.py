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


    