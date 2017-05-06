from bs4 import BeautifulSoup
import requests
import time
import json
import sys
import os
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

SITE = 'https://tw.user.mall.yahoo.com/rating/list?sid='
SITE_SEED = '&s=&b='

def get_last_page(seller):
	page_url = SITE + seller + SITE_SEED + '1'
	html_text = session.get(page_url, verify = True)
	soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
	class_found = soup.find('span', {'class': 'pagenum'}).getText()
	last_page_num = class_found.split(' ')[5]
	
	return last_page_num

def get_pages_url(seller):
	last_page = get_last_page(seller)
	pages = []
	for num in range(1, int(last_page) + 1):
		page_url = SITE + seller + SITE_SEED + str(num)
		pages.append(page_url)

	return pages

def get_comment():
	seller_id = 'ryoushoku'
	pages = get_pages_url(seller_id)

	for page in pages:
		html_text = session.get(page, verify = True)
		soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
		list_table_comment = soup.find('table', {'class': 'listtable'}).find('tbody')
		comments = list_table_comment.find_all('tr')
		for item in comments:
			print (item)
			break
		break

if __name__ == "__main__":
    session = requests.session()

    # get and store all buyer reviews
    get_comment()