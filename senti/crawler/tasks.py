from __future__ import absolute_import
from celery.decorators import task
from crawler.crawl_helper import *

@task
def crawl_products(category):
	crawl_product_list(category)

@task
def crawl_reviews(product):
	crawl_product_reviews(product)