#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:16:04 2020

@author: Cylita
"""

'''

Script for webscraping articles inserted into news stories by journalists. Articles scraped will be used to validate the approach chosen

'''

#Importing custom functions for analysis
from webscraping_funcs import ScrapeArticles
import pandas as pd

#Reading in csv file with data
news = pd.read_csv('/Users/Cylita/Desktop/insight-ds-project_news-link/data/processed/Cleaned_Split_RawNews.csv')
len(news)

#Creating a subset of the above stories to scrape for validation.
#Selecting the first 501 rows of data
news_subset = news.loc[0:500]
len(news_subset)

#From the above 501 stories I'm extracting the urls for news stories inserted by journalists
simurls = news['sim1']
#Cleaning urls to remove NA (missing)
cleanedurls =[x for x in simurls if str(x) != 'nan']
#Filtering to make sure all links have the proper start to them
urls_filtered = [link for link in cleanedurls if link.startswith('https://')]
len(urls_filtered)

#Scraping those articles for links inserted by journalists
cbc_validataion = ScrapeArticles(urls_filtered)

#Export to csv
cbc_validataion.to_csv('News_Raw_ValData.csv')
