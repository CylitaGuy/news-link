#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:16:04 2020

@author: Cylita
"""

#For webscraping similar articles
#Importing custom functions for analysis
from webscraping_funcs import ScrapeArticles
import pandas as pd

#Reading in csv file with data
news = pd.read_csv('/Users/Cylita/Desktop/insight-ds-project_news-link/data/processed/Cleaned_Split_RawNews.csv')
len(news)

#Creating a subset to valudate on because there is a lot of data currently
#selecting the first 501 rows of data
news_subset = news.loc[0:500]
len(news_subset)

#From the above 501 stories I'm
simurls = news['sim1']
cleanedurls =[x for x in simurls if str(x) != 'nan']
urls_filtered = [link for link in cleanedurls if link.startswith('https://')]
len(urls_filtered)

#Scraping those articles for the first inserted related link to validate
cbc_validataion = ScrapeArticles(urls_filtered)

#Writing daily export file to csv
cbc_validataion.to_csv('News_Raw_ValData.csv')
