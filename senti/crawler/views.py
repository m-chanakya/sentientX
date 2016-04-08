from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from crawler.crawl_helper import *
from crawler.api import *

# Create your views here.
def home(request):
	context = RequestContext(request, {'request': request})
	return render_to_response('crawler/home.html', context_instance=context)

def categories(request):
	context = RequestContext(request, {'request': request, 'data': render_categories()})
	return render_to_response('crawler/category.html', context_instance=context)

def products(request, category_id):
	category = get_object_or_404(Category, id = category_id)
	context = RequestContext(request, {'request': request, 'data': render_products(category)})
	return render_to_response('crawler/product.html', context_instance=context)

def reviews(request, product_id):
	product = get_object_or_404(Product, id = product_id)
	context = RequestContext(request, {'request': request, 'data': render_reviews(product)})
	return render_to_response('crawler/review.html', context_instance=context)

def crawl(request, type, id):
	if type == "category":
		category = get_object_or_404(Category, id = id)
		crawl_product_list(category)
		return redirect('categories')
	elif type == "product":
		product = get_object_or_404(Product, id = id)
		crawl_product_reviews(product)
		return redirect('home')
	return
