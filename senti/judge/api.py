from crawler.models import *

def render_category(category):
	return {
		'link': "/judge/products/"+str(category.id),
		'name': category.name,
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
		'link': "/judge/reviews/"+str(product.id)+"/0",
		'relink': "/judge/judge/product/"+str(product.id),
		'result_link': "/judge/result/product/"+str(product.id),
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
		'relink': "/judge/judge/review/"+str(review.id),
		'result_link': "/judge/result/review/"+str(review.id),
		'date': review.review_date,
		'author': review.author,
		'certified': review.certified_buyer,
		'product_rating': review.product_rating,
		'title': review.title,
		'desc': review.desc,
		'upvotes': review.upvotes,
		'total_votes': review.total_votes
	}

def render_reviews(product, start, PAGE_LEN):
	response = []
	for rev in Review.objects.filter(product= product)[start:start+PAGE_LEN]:
		response.append(render_review(rev))
	return response
