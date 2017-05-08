from bs4 import BeautifulSoup
import requests
import time
import json
import sys
import os
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

SITE = 'https://tw.user.mall.yahoo.com/'
INFO_FOOT = 'booth/view/stIntroMgt?sid='
COMMENT_SEED = 'rating/list?sid='
COMMENT_FOOT = '&s=&b='
SELLER_ID = str(sys.argv[1])
FIRST_PAGE_URL = SITE + COMMENT_SEED + SELLER_ID + COMMENT_FOOT + '1'

def get_info():
	page_url = SITE + INFO_FOOT + SELLER_ID
	html_text = session.get(page_url, verify = True)
	soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
	class_found = soup.find_all('div', {'class': 'bpgbd'}, 'html.parser')[-1]
	infos = class_found.find('ul').find_all('li')
	
	info_dic = {
		'seller_name': '-'.join(soup.find('title').getText().split('-')[:-1]),
		'corporation': infos[0].getText().split('：')[1],
		'representative': infos[1].getText().split('：')[1],
		'tel': infos[2].getText().split('：')[1],
		'fax': infos[3].getText().split('：')[1],
		'address': infos[4].getText().split('：')[1],
		'start_date': infos[5].getText().split('：')[1]
	}
	return info_dic

def get_last_page():
	html_text = session.get(FIRST_PAGE_URL, verify = True)
	soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
	class_found = FIRST_PAGE_SOUP.find('span', {'class': 'pagenum'}).getText()
	last_page_num = class_found.split(' ')[5]
	
	return last_page_num

def get_pages_url():
	last_page = get_last_page()
	pages = []
	for num in range(1, int(last_page) + 1):
		page_url = SITE + COMMENT_SEED + SELLER_ID + COMMENT_FOOT + str(num)
		pages.append(page_url)

	return pages

def check_good_store():
	class_found = FIRST_PAGE_SOUP.find('div', {'class': 'mainpane'})
	good_pic_alt = class_found.find('img')['alt']
	if good_pic_alt == '優良商店':
		return True
	else:
		return False

def get_comment():
	# seller_id = 'ryoushoku'
	pages = get_pages_url()
	good_store = check_good_store()

	comments_ary = []
	for page in pages:
		html_text = session.get(page, verify = True)
		soup = BeautifulSoup(html_text.text.encode('utf-8'), 'html.parser')
		list_table_comment = soup.find('table', {'class': 'listtable'}).find('tbody')
		comments = list_table_comment.find_all('tr')
		for item in comments:
			if good_store:
				score = item.find('em', {'class': 'store-sup'}).getText()
			else:
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
	
	return comments_ary	

def write_json_file(info, comments):

	info['seller_id'] = SELLER_ID
	info['comments'] = comments

	file_name = SELLER_ID + ' ' + str(time.strftime("%Y%m%d")) + '.json'
	comment_file = open('json/' + file_name, 'w', encoding='utf-8')
	comment_file.write(json.dumps(info, indent=4, ensure_ascii=False))
	comment_file.close()

if __name__ == "__main__":
    session = requests.session()

    FIRST_PAGE_HTML = session.get(FIRST_PAGE_URL, verify = True)
    FIRST_PAGE_SOUP = BeautifulSoup(FIRST_PAGE_HTML.text.encode('utf-8'), 'html.parser')

    # get seller's information
    info = get_info()

    # get and store all buyer reviews
    comments = get_comment()

    write_json_file(info, comments)
