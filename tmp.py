import io
import re
import requests
from bs4 import BeautifulSoup
#check for redirecting error, stops after 30 redirects
try:
	for i in range(50):
		r= requests.get("http://www.moneycontrol.com/stocks/company_info/stock_news.php?sc_id=GAC&scat=&pageno={}&next=0&durationType=Y&Year=2016&duration=1&news_type=".format(i), allow_redirects = False)
		soup = BeautifulSoup(r.content,"lxml")
		links =soup.find_all("a", {"class": "arial11_summ"})
		unique_links = list(set(links))
		for link in unique_links:
       			new = "https://www.moneycontrol.com"+link.get("href")
			result = requests.get(new,allow_redirects=True)
			try:
				data_text = BeautifulSoup(result.content,"lxml")
				extract_text = data_text.find(class_ = 'arti-flow')
				print extract_text.get_text()
				news = data_text.p    #only 1st paragraph
				text_data = news.get_text()
				print text_data
				print '\n'
				x = extract_text.get_text()
		 		y=x.split()
				m = y[0]
				d = y[1]
				year = y[2]
				dict = {'Jan': '01', 'Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
				y = dict[m]
				file_name = '%s-%s-%s'%(year,y,d)
				file_name = file_name.replace(',','')
				f = open(file_name, "a+")	
				f.write((text_data).encode('utf-8'))
				f.write('\n\n')
				f.close()
			except AttributeError:
				print '\n'
except requests.exceptions.TooManyRedirects as exc : 
	r = exc.response
	