import urllib2
from bs4 import BeautifulSoup
from datetime import datetime
import time
from crawler.models import *

BASE_URL = "http://www.flipkart.com"
GET_CAT_URL = "http://www.flipkart.com/footwear/pr?sid=osp"
AJAX_URL = "http://www.flipkart.com/lc/pr/pv1/spotList1/spot1/productList"

def crawl_product_reviews(product):
	'''
		Crawls user reviews 
		of a given product
	'''
	count = 0
	link = product.link
	no_of_tries = 0
	while link:
		print link
		try:
			response = urllib2.urlopen(link, timeout=5)
		except:
			if no_of_tries == 5:
				return {'status': 1, 'msg': 'URL open error'}
			no_of_tries += 1
			time.sleep(1)
			continue

		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		review_divs = soup.find_all(lambda tag: tag.name=='div' and ('review-id' in tag.attrs))

		for review_div in review_divs:
			review_id = review_div['review-id']
			review = Review.objects.filter(review_id = review_id)
			if review.exists():
				continue
			review = {'product': product, 'review_id': review_id}
			review['author'] = review_div.find('div', {'class': "unit size1of5 section1"}).find_all('div', {'class': 'line'})[1].text.strip()
			if review_div.find('img', {'alt': 'certified buyer1'}):
				review['certified_buyer'] = True
			review['review_date'] = datetime.strptime(review_div.find('div', {'class' : "date line fk-font-small"}).text.strip(), "%d %b %Y")
			review['product_rating'] = int(review_div.find('div', {'class':'fk-stars'})['title'].split()[0])
			review['title'] = review_div.find('div', {'class' : 'line fk-font-normal bmargin5 dark-gray'}).text.strip()
			review['desc'] = review_div.find('span', {'class' : 'review-text'}).text.strip()
			review_rating = review_div.find('div', {'class' : 'line fk-font-small review-status-bar'}).find('div', {'class' : 'unit'}).find_all('strong')
			review['total_votes'] = int(review_rating[1].text)
			if review_rating[0].text.endswith("%"):
				review['upvotes'] = round((int(review_rating[0].text[:-1])*review['total_votes'])/100)
			else:
				review['upvotes'] = int(review_rating[0].text)
			count += 1
			Review.objects.create(**review)

		next = ''
		out_links = soup.find_all('a', {'class': 'nav_bar_next_prev'})
		for link in out_links:
			if link.text.strip().startswith('Next Page'):
				next = BASE_URL + link['href']
		link = next
		no_of_tries = 0
		print count
	return {'status': 0, 'msg': 'Success', 'count': count}


def crawl_product_list(category):
	'''
		Crawls list of products 
		in a given category
	'''
	def _create_review_url(url):
		parts = url.split('/')[1:]
		return '/'.join( [parts[0], 'product-reviews', parts[2].split('&')[0] ] )

	link = BASE_URL + category.link
	count = 0
	no_of_tries = 0
	while link:
		print link
		try:
			response = urllib2.urlopen(link, timeout=5)
		except:
			if no_of_tries == 5:
				return {'status': 1, 'msg': 'URL open error'}
			no_of_tries += 1
			continue

		if response.code != 200:
			break

		html = response.read()
		soup = BeautifulSoup(html, "html.parser")
		product_divs = soup.find_all('a', {'data-tracking-id': 'prd_title'})

		for product_div in product_divs:
			data = {'category': category}
			data['name'] = product_div['title']
			product = Product.objects.filter(name = data['name'])
			if product.exists():
				continue
			data['link'] = _create_review_url(product_div['href'])
			Product.objects.create(**data)
			count += 1

		sid = category.sid
		start = str(count + 1)
		filterNone = "true"
		ajax = "true"
		link = AJAX_URL + '?' + '&'.join(["sid="+sid, "start="+start, "filterNone="+filterNone, "ajax="+ajax])
		no_of_tries = 0
		print count
	return {'status': 0, 'msg': 'Success', 'count': count}
			

def crawl_categories():
	def _create_product_list_url(url, sid):
		return url + "?sid=" + sid
	print GET_CAT_URL
	try:
		response = urllib2.urlopen(GET_CAT_URL, timeout=5)
	except:
		return {'status': 1, 'msg': 'URL open error'}
	html = response.read()
	soup = BeautifulSoup(html, "html.parser")
	cats = soup.find('form', {'action': '/search'}).find('select').find_all('option')
	for cat in cats:
		data = {}
		data['sid'] = cat['data-storeid']
		category = Category.objects.filter(sid = data['sid'])
		if category.exists():
			continue
		data['name'] = cat.text.strip()
		data['link'] = _create_product_list_url(cat['data-storeurl'], cat['data-storeid'])
		Category.objects.create(**data)

# def main():
# 	print crawl_product_list(category)

# if __name__ == "__main__":
# 	main()

