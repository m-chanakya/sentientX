from django.shortcuts import render_to_response
from django.template import RequestContext
from crawler.models import *
from crawler.crawl_helper import *
from crawler.api import *

# Create your views here.
def home(request):
	context = RequestContext(request, {'request': request})
	return render_to_response('crawler/home.html', context_instance=context)

def categories(request):
	context = RequestContext(request, {'request': request, 'data': render_categories()})
	return render_to_response('crawler/category.html', context_instance=context)

def products(request):
	#context = RequestContext(request, {'request': request, 'data': render_products()})
	return render_to_response('crawler/product.html', context_instance=context)

def reviews(request):
	#context = RequestContext(request, {'request': request, 'data': render_reviews()})
	return render_to_response('crawler/review.html', context_instance=context)