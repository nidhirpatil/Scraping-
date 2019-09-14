import requests
import re
import codecs
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome('/home/nidhi/chromed/chromedriver')
url = u'https://twitter.com/realDonaldTrump'
browser.get(url)
time.sleep(1)
body = browser.find_element_by_tag_name('body')

for _ in range(10000):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)

tweets = browser.find_elements_by_class_name('tweet-text')

f=codecs.open("file1.txt","w")
for tweet in tweets:
    try:
    	print(tweet.text)
    #ntweet = u' '.tweet.encode('utf-8').strip()
   # ntweet = tweet.encode('utf-8')
   # ntweet = str.encode(encoding="utf-8", errors="strict")
    	f.write(tweet.text)
    	f.write('\n\n')
    	print('\n\n')
    except:
    	print('\n')
f.close();
