from django.shortcuts import render_to_response
from django.template import RequestContext
from crawler.models import *
from crawler.crawl_helper import *

# Create your views here.
def home(request):
	context = RequestContext(request, {'request': request})
	return render_to_response('crawler/home.html', context_instance=context)

def category(request):
