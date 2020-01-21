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
import time


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
    for story in np.arange(0, len(headlines)):
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
#Function which requests specific details from article urls provide to it
def ScrapeArticles(arts):
    #Creating empty lists for article details that need to be stored
    authname =[]
    date = []
    title = []
    maintext = []
    mainurl =[]
    simlinks = []
    relalinks = []
    
    #Extracting relevant details from stories of interest
    for link_no in np.arange(0, len(arts)):
        #Requesting article link and creating content soup
        link = arts[link_no]
        #Adding in a pause in the code
        time.sleep(3)
        #Specify headers
        headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        art = requests.get(link, headers = headers)
        art_soup = BeautifulSoup(art.content, 'html5lib')
    
        #Add url to new list
        mainurl.append(link)
        
        #Finding and adding authours
        try:
            author = art_soup.find('span', class_='authorText').get_text()
        except:
            author = "Anonymous"
        
        authname.append(author)
        
        #Finding and adding publication date
        pub_time = art_soup.find('time', class_='timeStamp')['datetime']
        date.append(pub_time)
        
        #Finding and adding article title
        art_title = art_soup.find('h1', class_='detailHeadline').get_text()
        title.append(art_title)
        
        #Finding and adding similar article links if present
        try: 
            s_links = art_soup.find_all('a', class_='similarLink')
            s_urls_temp = []
            s_urls = []
            for similar in np.arange(0, len(s_links)):
                linklist = s_links[similar]['href']
                s_urls_temp.append(linklist)
                s_urls = " ".join(s_urls_temp)    
        except:
            s_urls = "N/A"
        
        simlinks.append(s_urls)
        
        #Finding and adding related article links if present
        try:
            r_links=art_soup.find_all('a', class_='relatedLink')
            r_urls_temp = []
            for related in np.arange(0, len(r_links)):
                linkrlist = r_links[related]['href']
                r_urls_temp.append(linkrlist)
                r_urls = " ".join(r_urls_temp)
                
        except:
            r_urls = "N/A"
        
        relalinks.append(r_urls)
        
        #Scraping the actual paragraphs of the story of interest
        body = art_soup.find_all('div', class_='story')
        x = body[0].find_all('p')
    
        list_paras = []
        for para in  np.arange(0, len(x)):
            paragraph = x[para].get_text()
            list_paras.append(paragraph)
            final_article =" ".join(list_paras)
            
        maintext.append(final_article)
            
    #Now converting all lists into a pandas dataframe to be returned
    df = pd.DataFrame(list(zip(authname, date,title, maintext, mainurl, simlinks, relalinks)), 
                  columns = ['author', 'date', 'title', 'maintext','mainurl','simlinks','relalinks'])

    return df
