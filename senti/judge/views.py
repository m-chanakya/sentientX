from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from judge.models import *
from crawler.models import *
from .tasks import *
from .api import *
import json

def categories(request):
	context = RequestContext(request, {'request': request, 'data': render_categories()})
	return render_to_response('judge/category.html', context_instance=context)

def products(request, category_id):
	category = get_object_or_404(Category, id = category_id)
	context = RequestContext(request, {'request': request, 'data': render_products(category), 'category': category.name})
	return render_to_response('judge/product.html', context_instance=context)

def reviews(request, product_id, start):
	product = get_object_or_404(Product, id = product_id)

	start = int(start)
	PAGE_LEN = 20
	if start < len(Review.objects.filter(product= product)):
		next = "/judge/reviews/"+str(product_id)+"/"+str(start+PAGE_LEN)
	else:
		next = None
	if start >= 20:
		prev = "/judge/reviews/"+str(product_id)+"/"+str(start-PAGE_LEN)
	else:
		prev = None

	context = RequestContext(request, {'request': request, 'data': render_reviews(product, start, PAGE_LEN), \
		'product': product.name, 'next': next, 'prev': prev})
	return render_to_response('judge/review.html', context_instance=context)

def results(request, type, id):
	if type == "product":
		product = get_object_or_404(Product, id = id)
		judge = get_object_or_404(ProductJudgement, product = product)
	elif type == "review":
		print "IAM HERE", type, id
		review = get_object_or_404(Review, id = id)
		print review.title
		judge = get_object_or_404(ReviewJudgement, review = review)
	
	data = json.loads(judge.judgement)
	x = []
	y = []
	for each in data:
		x.append(each)
		y.append(data[each][0])
	context = RequestContext(request, {'request': request, 'x': json.dumps(x), 'y': json.dumps(y)})
	return render_to_response('judge/result.html', context_instance=context)

def judge(request, type, id):
	if type == "product":
		product = get_object_or_404(Product, id = id)
		judge_product(product = int(id))
	elif type == "review":
		review = get_object_or_404(Review, id = id)
		judge_review(review = int(id))
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))