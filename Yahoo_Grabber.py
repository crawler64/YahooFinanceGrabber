import urllib3
import certifi
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def csv_write_header(filename):
	with open(filename, 'wb') as csv_file:
		writer = csv.writer(csv_file, lineterminator='\n')
		writer.writerow(["Stockname", "Date of dividend distribution", "Expected dividend absolute", "Expected dividend relative (%)"])
	return

def BS_getData(rlinks):
	soup_links = BeautifulSoup(rlinks.data, 'html.parser')
	return soup_links
	
def init_urllib3(url):
	http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
	rlinks = http.request('GET', url)
	return rlinks

csvfile = 'index.csv'
url = ['https://de.finance.yahoo.com/most-active?failsafe=1&ynet=0&_device=desktop&device=desktop&offset=0&count=200','https://de.finance.yahoo.com/most-active?failsafe=1&ynet=0&_device=desktop&device=desktop&offset=200&count=200']
csv_write_header(csvfile)

#iterate over url list
for url_links in url:
	soup_links = BS_getData(init_urllib3(url_links))				
	for rlinks in soup_links.find_all('a', href=True, attrs={'class':'Fw(600)'}):
		thisurl =  "https://de.finance.yahoo.com" + rlinks['href']
		r = init_urllib3(thisurl)
		soup = BS_getData(r)

		#find name of stock
		for link in soup.find_all('div', attrs={'class':'D(ib)'}):
			if link.find_all('h1', attrs={'class':'D(ib) Fz(18px)'}) != []:
				print link.find_all('h1', attrs={'class':'D(ib) Fz(18px)'})[0].text
				stockname = link.find_all('h1', attrs={'class':'D(ib) Fz(18px)'})[0].text.encode('utf-8')
				break
		
		#find expected dividends
		try:
			price = soup.find_all('td', attrs={'data-test':'DIVIDEND_AND_YIELD-value'})[0].text.replace(',','.').replace('(','').replace(')','').replace('%','').split()
		except IndexError:
			print "--"
			
		#find date of dividend distribution
		try:
			print(soup.find_all('td', attrs={'data-test':'EX_DIVIDEND_DATE-value'})[0].find('span').text)
			dividenddate = soup.find_all('td', attrs={'data-test':'EX_DIVIDEND_DATE-value'})[0].find('span').text
			if price != "" and price != "N/A" and dividenddate != "" and dividenddate != "N/A":
				with open('index.csv', 'a') as csv_file:
					writer = csv.writer(csv_file, lineterminator='\n')
					writer.writerow([stockname, dividenddate, price[0], price[1]])
		except IndexError:
			print "--"
