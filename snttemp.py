import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime


start_date = '2018-02-21'
end_date = '2019-05-31'
daterange = pd.date_range(start_date,end_date)
stock_list = ['AMBUJACEM','ASIANPAINT','AUROPHARMA','AXISBANK','BAJFINANCE','BPCL','BOSCHLTD','CIPLA','DRREDDY','EICHERMOT','GAIL','HCLTECH','HDFCBANK','HEROMOTOCO','HINDALCO','HINDPETRO','HINDUNILVR','HDFC','ITC','ICICIBANK','IOC','INDUSINDBK','INFY','KOTAKBANK','LT','LUPIN','M&M','MARUTI','NTPC','ONGC','POWERGRID','RELIANCE','SBIN','SUNPHARMA','TCS','TATAMOTORS','TATASTEEL','TECHM','UPL','ULTRACEMCO','VEDL','WIPRO','YESBANK','ZEEL']
stock_list2 = ['GAC','API','AP','UTI10','BAF','BPC','MIC','C','DRL','EM','GAI','HCL02','HDF01','HHM','H','HPC','HL','HDF','ITC','ICI02','IOC','IIB','IT','KMF','LT','LC03','MM','MU01','NTP','ONG','PGC','RI','SBI','SPI','TCS','TEL','TIS','TM4','SI10','UTC','SG','W','YB','ZT']


lookback = 3
url_lib = []
for symbol in stock_list2:
	url_lib.append("http://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id={}&durationType=M&duration=6".format(symbol))
	
print url_lib
def load_positive():
	myfile = open("/home/harsha/projects/trading/sentd/positive.csv","r")
	positives = myfile.readlines()
	positive = [pos.strip().lower() for pos in positives]
	return positive
	
def load_negative():
	myfile = open("/home/harsha/projects/trading/sentd/negative.csv" ,"r")
	negatives = myfile.readlines()
	negative = [neg.strip().lower() for neg in negatives]
	return negative
	


def countNeg(cleantext, negative):
    """
    counts negative words in cleantext
    """
    negs = [word for word in cleantext if word in negative]
    return len(negs)



def countPos(cleantext, positive):
    """
    counts negative words in cleantext
    """
    pos = [word for word in cleantext if word in positive]
    return len(pos)  





def getSentiment(cleantext, negative, positive):
    """
    counts negative and positive words in cleantext and returns a score accordingly
    """
    positive = load_positive()
    negative = load_negative()
    return (countPos(cleantext,positive) - countNeg(cleantext, negative))








base_url = "http://www.moneycontrol.com"
#url = "http://www.moneycontrol.com/company-article/statebankindia/news/SBI#SBI"


positive = load_positive()
negative = load_negative()




def senti_generator(url,positive,negative,lookback):
	
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")

	list_of_links = []
	sublinks = soup.find_all("a", {"class": "arial11_summ"})
	#sublinks = links.find_all("s",{"class" : "arial11_summ"})
	for links in sublinks:
		sp = BeautifulSoup(str(links),'html.parser')
		tag = sp.a
		list_of_links.append(base_url + tag["href"])
	
	unique_links = ((list_of_links))

	final_links = unique_links[0:lookback]

	snt_score = 0
	for x in final_links:
		result_url = x
		result = requests.get(result_url)
		result_text = BeautifulSoup(result.text,"lxml")
		extract_text = result_text.find(class_ = 'article_box')
		text = extract_text.get_text()
		from nltk.tokenize import RegexpTokenizer
		tokenizer = RegexpTokenizer(r'\w+')
		text = tokenizer.tokenize(text)
		from nltk.corpus import stopwords
		clean = [word for word in text if word not in stopwords.words('english')]
		print clean,"\n\n"
		snt_score = snt_score+getSentiment(clean,negative,positive)
	return snt_score
		
#g_data = soup.find_all("div",{"class": "FL"})	

#sub_links[]

#for item in g_data:
#	 item.find_all("a", {"class": "arial11_summ"})

#class FinancecrawlerItem(scrapy.Item):
#	date = scrapy.Field()
#	keywords = scrapy.Field()
#	body = scrapy.Field()
weights = []
def append_senti(url_lib,weights,positive,negative,lookback,stock_list):
	count = 0
	df1 = pd.read_csv("~/projects/trading/sentiment_result/sentiment_score.csv",index_col = 'Date', parse_dates = True)
	for url in url_lib:
		weights.append(senti_generator(url,positive,negative,lookback))
		print senti_generator(url,positive,negative,lookback),url
	weights = np.asarray(weights)
	df2 = pd.DataFrame(weights,columns = stock_list)
	df2 = df1.append(df2,ignore_index = True)
	df2.to_csv("~/projects/trading/sentiment_result/sentiment_score.csv")
	

append_senti(url_lib,weights,positive,negative,lookback,stock_list)
stock_list2 = ['GAC','API','AP','UTI10','BAF','BPC','MIC','C','DRL','EM','GAI','HCL02','HDF01','HHM','H','HPC','HL','HDF','ITC','ICI02','IOC','IIB','IT','KMF','LT','LC03','MM','MU01','NTP','ONG','PGC','RI','SBI','SPI','TCS','TEL','TIS','TM4','SI10','UTC','SG','W','YB','ZT']


pharma = ["CIPLA","AUROPHARMA","DRREDDY","LUPIN","SUNPHARMA"]
it = ["HCLTECH","INFY","TCS","TECHM","WIPRO"]
cements = ["AMBUJACEM","ULTRACEMCO"]
automobile = ["BAJAJ-AUTO","BOSCHLTD","HEROMOTOCO","M&M","MARUTI","EICHERMOT","TATAMOTORS"]
finserv = ["AXISBANK","BANKBARODA","BAJFINANCE","HDFC","HDFCBANK","ICICIBANK","IBULHSGFIN","INDUSINDBK","KOTAKBANK","SBI","YESBANK"]
metals = ["HINDALCO","TATASTEEL","VEDL"]
energy = ["BPCL","GAIL","IOC","NTPC","ONGC","POWERGRID","RELIANCE","HINDPETRO"]
consumer_goods = ["ASIANPAINT","HINDUNILVR","ITC"]
construction = ["LT"]
media = ["ZEEL"]
agri = ["UPL"]
	
