from crawler.models import *

def render_category(category):
	return {
		'link': "http://localhost:8002/crawler/products/"+str(category.id),
		'name': category.name,
		'relink': "http://localhost:8002/crawler/crawl/category/"+str(category.id),
		'date': category.crawled_date,
		'total': len(Product.objects.filter(category= category))
	}

def render_categories():
	response = []
	for cat in Category.objects.all():
		response.append(render_category(cat))
	return response

def render_product(product):
	return {
		'link': "http://localhost:8002/crawler/reviews/"+str(product.id),
		'relink': "http://localhost:8002/crawler/crawl/product/"+str(product.id),
		'name': product.name,
		'date': product.crawled_date,
		'total': len(Review.objects.filter(product= product))
	}

def render_products(category):
	response = []
	for prod in Product.objects.filter(category= category):
		response.append(render_product(prod))
	return response

def render_review(review):
	return {
		'date': review.review_date,
		'author': review.author,
		'certified': review.certified_buyer,
		'product_rating': review.product_rating,
		'title': review.title,
		'desc': review.desc,
		'upvotes': review.upvotes,
		'total_votes': review.total_votes
	}

def render_reviews(product):
	response = []
	for rev in Review.objects.filter(product= product):
		response.append(render_review(rev))
	return response
