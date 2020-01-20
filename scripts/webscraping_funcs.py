#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 10:37:53 2020

@author: Cylita
"""

'''
Functions file for web scraping articles

'''
#Required packages
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup


###########Func 1
#Function for pulling all story urls from a website landing page

def ScrapeCover(url):
    #Grab content from webpage of interest and convert to soup
    news_page = requests.get(url)
    news_soup = BeautifulSoup(news_page.content, 'html5lib')
    
    #Extracting all news headlines from html soup
    headlines = news_soup.find_all('a', class_='card')
    
    #Create empty list for storing story urls
    coverpage_urls =[]
    
    #Extracting coverpage news urls from html soup
    for story in np.arrange(0, len(headlines)):
        story_url = headlines[story]['href']
        coverpage_urls.append(story_url)
    
    #Not all urls have the full proper website link, creating a function to check
    def containsURL(str, set='https://www.cbc.ca'):
        for c in set:
            if c not in str: return 0
        return 1
    
    #Defining a function that assigns proper front portion of link if missing
    def replaceURL(link):
        if containsURL(link)==0:
            return ('https://www.cbc.ca'+ link)
        else:
            return link
        
    #Creating complete list of full story urls
    complete_urls = list(map(replaceURL, coverpage_urls))
   
    #Return the list of news link from the function
    return complete_urls
    
#########Func 2
    
    