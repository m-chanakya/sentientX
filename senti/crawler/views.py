from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.template import RequestContext
from crawler.api import *
from crawler.models import *
from crawler.tasks import *
from django.utils import timezone

# Create your views here.
def home(request):
	context = RequestContext(request, {'request': request})
	return render_to_response('crawler/home.html', context_instance=context)

def categories(request):
	context = RequestContext(request, {'request': request, 'data': render_categories()})
	return render_to_response('crawler/category.html', context_instance=context)

def products(request, category_id):
	category = get_object_or_404(Category, id = category_id)
	context = RequestContext(request, {'request': request, 'data': render_products(category), 'category': category.name})
	return render_to_response('crawler/product.html', context_instance=context)

def reviews(request, product_id, start):
	product = get_object_or_404(Product, id = product_id)

	start = int(start)
	PAGE_LEN = 20
	if start < len(Review.objects.filter(product= product)):
		next = "http://localhost:8000/crawler/reviews/"+str(product_id)+"/"+str(start+PAGE_LEN)
	else:
		next = None
	if start >= 20:
		prev = "http://localhost:8000/crawler/reviews/"+str(product_id)+"/"+str(start-PAGE_LEN)
	else:
		prev = None

	context = RequestContext(request, {'request': request, 'data': render_reviews(product, start, PAGE_LEN), \
		'product': product.name, 'next': next, 'prev': prev})
	return render_to_response('crawler/review.html', context_instance=context)

def crawl(request, type, id):
	if type == "category":
		category = get_object_or_404(Category, id = id)
		category.crawled_date = timezone.now()
		category.save()
		crawl_products.delay(category = int(id))
	elif type == "product":
		product = get_object_or_404(Product, id = id)
		product.crawled_date = timezone.now()
		product.save()
		crawl_reviews.delay(product = int(id))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
