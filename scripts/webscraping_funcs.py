#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 10:37:53 2020

@author: Cylita
"""

'''
Functions file for web scraping articles from all major CBC landing pages

'''
#Importing required packages
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
from requests.exceptions import ConnectionError

###########Function 1:
#Function pulls all story urls from a website's landing page

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
    def containsURL(url, homelink='https://www.cbc.ca'):
        for char in homelink: 
            if char not in url: return 0
        return 1
    
    #Defining a function that assigns proper front portion of link if missing
    def replaceURL(link):
        if containsURL(link)==0:
            return ('https://www.cbc.ca'+ link)
        else:
            return link
    
    #Creating complete list of full story urls
    complete_urls = list(map(replaceURL, coverpage_urls))
    
    try:
        #removing problematic link if present from the complete urls list
        complete_urls.remove('https://www.cbc.cahttps://cbc.radio-canada.ca/en/ombudsman/')
    except (ValueError):
        #If problematic link not present, continue
        pass
    #Return the list of news link from the function
    return complete_urls
    
#########Function 2:
#Function pulls specific details from an article url passed to it

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
        time.sleep(1)
        #Specify headers
        headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
        try:
            art = requests.get(link, headers = headers)
        except ConnectionError as e:
            pass

        art_soup = BeautifulSoup(art.content, 'html5lib')
    
        #Add url to new list
        mainurl.append(link)
        
        #Finding and adding authors
        try:
            author = art_soup.find('span', class_='authorText').get_text()
        except:
            author = "Anonymous"
        
        authname.append(author)
        
        #Finding and adding publication date
        try:
            pub_time = art_soup.find('time', class_='timeStamp')['datetime']
        except:
            pub_time="N/A"
            
        date.append(pub_time)
        
        #Finding and adding article title
        try:
            art_title = art_soup.find('h1', class_='detailHeadline').get_text()
        except:
           art_title="N/A" 
        
        title.append(art_title)
        
        #Finding and adding similar article links if present
        try: 
            s_links = art_soup.find_all('a', class_='similarLink')
            
            s_urls_temp = []
            
            s_urls=[]
            
            for similar in np.arange(0, len(s_links)):
                linklist = s_links[similar]['href'] #for each link in html soup, get url of similar link
                s_urls_temp.append(linklist) #add url to list
                s_urls = " ".join(s_urls_temp) #join all similar urls (eventually creates a list within a list) 
        except:
            s_urls = "N/A"
        
        simlinks.append(s_urls)
        
        #Finding and adding related article links if present
        try:
            r_links=art_soup.find_all('a', class_='relatedLink')
            
            r_urls_temp = []
            
            r_urls = []
            
            for related in np.arange(0, len(r_links)):
                linkrlist = r_links[related]['href'] #for each link in html soup, get url of related story links
                r_urls_temp.append(linkrlist) #add url to the list
                r_urls = " ".join(r_urls_temp) #join all similar urls (eventually creates a list within a list)
        except:
            r_urls = "N/A"
        
        relalinks.append(r_urls)
        
        #Scraping the actual paragraphs of the story of interest
        try:
            body = art_soup.find_all('div', class_='story')
            story = body[0].find_all('p')
    
            list_paras = []

            for para in  np.arange(0, len(story)):
                paragraph = story[para].get_text() #get paragraph text
                list_paras.append(paragraph) #add paragraph to list
                final_article =" ".join(list_paras) #join all paragraphs with a space
        except:
            final_article = "N/A"
            
        maintext.append(final_article)
            
    #Now converting all lists into a pandas dataframe to be returned
    df = pd.DataFrame(list(zip(authname, date,title, maintext, mainurl, simlinks, relalinks)), 
                  columns = ['author', 'date', 'title', 'maintext','mainurl','simlinks','relalinks'])

    return df



