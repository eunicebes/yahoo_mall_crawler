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
SELLER_ID = str(sys.argv[1])
FIRST_PAGE_URL = SITE + SELLER_ID + SITE_SEED + '1'

def get_seller_name():
	html_text = session.get(FIRST_PAGE_URL, verify = True)
	soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
	name = soup.find('title').getText().split('-')[0]

	return name

def get_last_page():
	html_text = session.get(FIRST_PAGE_URL, verify = True)
	soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
	class_found = soup.find('span', {'class': 'pagenum'}).getText()
	last_page_num = class_found.split(' ')[5]
	
	return last_page_num

def get_pages_url():
	last_page = get_last_page()
	pages = []
	for num in range(1, int(last_page) + 1):
		page_url = SITE + SELLER_ID + SITE_SEED + str(num)
		pages.append(page_url)

	return pages

def get_comment():
	# seller_id = 'ryoushoku'
	seller_name = get_seller_name()
	pages = get_pages_url()

	comments_ary = []
	for page in pages:
		html_text = session.get(page, verify = True)
		soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
		list_table_comment = soup.find('table', {'class': 'listtable'}).find('tbody')
		comments = list_table_comment.find_all('tr')
		for item in comments:
			score = item.find('em', {'class': 'store'}).getText()
			content = item.find('dl', {'class': 'comment'}).find('dd').getText()
			buyer_id = item.find_all('td')[-1].getText()
			date = item.find('th').getText()

			comment = {
				'score': score,
				'content': content,
				'buyer_id': buyer_id,
				'date': date
			}
			
			comments_ary.append(comment)

			print (buyer_id)			
	
	comments_per_shop = {
		'seller_id': SELLER_ID,
		'seller_name': seller_name,
		'comments': comments_ary
	}	

	file_name = SELLER_ID + ' ' + str(time.strftime("%Y%m%d")) + '.json'
	comment_file = open('json/' + file_name, 'w', encoding='utf-8')
	comment_file.write(json.dumps(comments_per_shop, indent=4, ensure_ascii=False))
	comment_file.close()


if __name__ == "__main__":
    session = requests.session()

    # get and store all buyer reviews
    get_comment()