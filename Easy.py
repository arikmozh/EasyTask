# OS module in Python provides functions for interacting with the operating system.
import os 
# sync_playwright module for inspecting a dynamic page.
from playwright.sync_api import sync_playwright
# BeautifulSoup module for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup 
# Pandas module data manipulation and analysis used for exporting json to CSV file.
import pandas as pd
# JSON module for working with json data.
import json 

class Easy:
  def __init__(self,key_word):
    self._url = 'https://easy.co.il/search/%20' # easy.co.il url
    self.key_word = key_word # topic you searching for
    self.results = {} # the results dict from easy
    self.index = 0 # counting the key in results dict
    self.title = '' # page title
  
  def run(self):
    with sync_playwright() as p:
      browser = p.chromium.launch()
      page = browser.new_page()
      page.goto(self._url+self.key_word) 
      html = page.inner_html('#listResults') # main div id where all cards placed.
      soup = BeautifulSoup(html,'html.parser')  
      self.title = page.title() # get Title from the page.
      cards = soup.find_all('a',{'class':'biz-item-link-wrapper reg'}) # object with all specific data.
      browser.close()

      for card in cards:
        c = {} # storing each card data into a dict.

        c['distance'] = card.find('div',{'class':'biz-list-marker'}).text
        c['name'] = card.find('p',{'class':'biz-list-name'}).text
        c['class'] = card.find('p',{'class':'biz-list-class'}).text
        c['address'] = card.find('p',{'class':'biz-list-address'}).text

        # not every card have a review.
        try:
          c['reviews'] = card.find('div',{'class':'biz-list-review-snippet'}).text
        except:
          pass
        try:
          c['rates'] = card.find('div',{'class':'biz-prop-wrapper'}).text
        except:
          pass
        try:
          c['isOpen'] = card.find('div',{'class':'biz-list-hours hours-text'}).text
        except:
          pass  

        self.results[self.index] = c # adding the card data into dict with key: index, value: {distance: x, name: y, class: z...}
        self.index+=1
      self.save_to_csv() # calling save_to_csv func

  def save_to_csv(self): 
    dir_path = os.path.dirname(os.path.realpath(__file__)) # return your exact path.
    json_obj = json.dumps(self.results,ensure_ascii=False) # converting dict to json.
    pdObj = pd.read_json(json_obj, orient='index') # opening json with pandas to read.
    csv = pdObj.to_csv('csv/{0}.csv'.format(self.title),index=False,encoding='utf-8-sig',header=True) # saving into csv format.
    print('\ncsv is saved in dir - '+dir_path+'/csv')


