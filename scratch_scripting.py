#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 14:51:33 2020

@author: Cylita
"""

def hello():
  
    print("Hello Spencer")
    
hello()

name = "Derek"
print (name)


import random
import os
import sys

list_test = ['juice', 'potatoes']

list_test.append = ['pickle']
del list_test[0]
print(list_test)

age = 15

random_num = random.randrange(0,15)

print(random_num)

while(random_num !=50):
    print (random_num)
    random_num = random.randrange(1,60)

def addNumber(fNum, lNum):
    sumNum=fNum+lNum
    return sumNum

print(addNumber(1,5))

string = addNumber (1,3)

import time
from selenium import webdriver

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.get('https://www.thestar.com/sports/bluejays/2020/01/18/the-blue-jays-are-back-in-powder-blue-at-least-some-of-the-time.html')

cbc='https://www.cbc.ca/news/canada/british-columbia/wet-suwet-en-elder-calls-for-dialogue-as-pipeline-polarizes-some-in-northern-british-columbia-1.5432262'
driver.get(cbc)

userid_element = driver.find_elements_by_xpath('//*[@id="Comment_5561090"]/div/div[2]/div[1]/span[1]/a[2]')[0]
userid = userid_element.text

