#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 16:20:31 2020

@author: Cylita
"""

'''

Script contains functions that are meant to scrape the CBC news website for
article data.

'''
#Importing custom functions for analysis
from webscraping_funcs import ScrapeCover
from webscraping_funcs import ScrapeArticles
import pandas as pd

'''
Script for scraping CBC news landing page for daily articles
'''

#Creating an empty pandas dataframe to store updated daily results
df_store = pd.DataFrame(columns = ['author', 'date', 'title', 'maintext','mainurl','simlinks','relalinks'])

#Creating a list of major CBC news landing pages
cbc_landings = [
        'https://www.cbc.ca/news',
        'https://www.cbc.ca/news/canada/ottawa',
        'https://www.cbc.ca/news/canada/british-columbia',
        'https://www.cbc.ca/news/canada/calgary'
        'https://www.cbc.ca/news/canada/edmonton',
        'https://www.cbc.ca/news/canada/saskatchewan',
        'https://www.cbc.ca/news/canada/montreal',
        'https://www.cbc.ca/news/canada/new-brunswick',
        'https://www.cbc.ca/news/canada/prince-edward-island',
        'https://www.cbc.ca/news/canada/nova-scotia',
        'https://www.cbc.ca/news/canada/newfoundland-labrador',
        'https://www.cbc.ca/news/canada/north',
        'https://www.cbc.ca/news/opinion',
        'https://www.cbc.ca/news/world',
        'https://www.cbc.ca/news/canada',
        'https://www.cbc.ca/news/politics',
        'https://www.cbc.ca/news/indigenous',
        'https://www.cbc.ca/news/business',
        'https://www.cbc.ca/news/health',
        'https://www.cbc.ca/news/entertainment',
        'https://www.cbc.ca/news/technology',
        'https://www.cbc.ca/news/investigates',
        'https://www.cbc.ca/news/gopublic'
        ]

#Looping Coverpage Scraping Function over cbc landing pages to get story urls
cbc_home_lists = list(map(ScrapeCover, cbc_landings))

#Flattening sublists of CBC news into a single list
cbc_home_urls = []
for sublist in cbc_home_lists:
    for item in sublist:
        cbc_home_urls.append(item)

#Extacting unique set of links
cbc_unique_stories = list(set(cbc_home_urls))

#Running article scraping function using list of isolated stories
cbc_data = ScrapeArticles(cbc_unique_stories)

#Append data for today to existing dataframe
daily_export = df_store.append(cbc_data)

#Writing daily export file to csv
daily_export.to_csv('Jan_21_news.csv')













    
    
    
    
    
    
    
    
    
    