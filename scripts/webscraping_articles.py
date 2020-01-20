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
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

'''
Script for scraping CBC news landing page for daily articles
'''

#Specifying news landing page (here CBC.ca news) and converting to soup
news_page = requests.get('https://www.cbc.ca/news')
news_soup = BeautifulSoup(news_page.content, 'html5lib')

#Extracting all news headlines from html soup
coverpage_news = news_soup.find_all('a', class_='card')

#Empyty list for storing story urls
news_url = []

#Extracting coverpage news story urls from html soup
for story in np.arange(0, len(coverpage_news)):
    url=coverpage_news[story]['href']
    news_url.append(url)

#Storing links in a dataframe and exporting as a csv
url_DF = pd.DataFrame({'url':news_url})
print(url_DF)
#Tomorrow write this into a fucntion and then 


#Now need to create a loop to extact info from news artcles of interest
#Creating articles for information need to store:

authorname = []
date = []
title = []
url = []
maintext = []
related_links = []


for link in news_url:
    #Requesting article via link and isolating html content
    article = requests.get(link)
    conent = article.content
    
    #Converting to soup

test=news_url[4]
print(test)    

article = requests.get(test)
content = article.content

test_soup = BeautifulSoup(content, 'html5lib')    
try:
    author = test_soup.find('span', class_='authorText').get_text()
except:
    aname = "Anonymous"    


pub_time = test_soup.find('time', class_='timeStamp').get_text()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    