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
#Importing custom functions file
import webscraping_funcs
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd

'''
Script for scraping CBC news landing page for daily articles
'''
#Specifying news landing page and feeding into function to extract stories

cbc_news = ['https://www.cbc.ca/news','https://www.cbc.ca/news/local']

cbc_



cbc_home = ScrapeCover(cbc_news)

cbc_data = ScrapeArticles(cbc_home)


export_csv = a.to_csv('test.csv')












    
    
    
    
    
    
    
    
    
    