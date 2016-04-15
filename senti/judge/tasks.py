from __future__ import absolute_import
from celery.decorators import task
from .judge_helper import judger
from crawler.models import *
from judge.models import *
from nltk.tokenize import sent_tokenize
import json

@task
def judge_review(review):
	review = Review.objects.get(id = review)
	print review.title
	judgement = ReviewJudgement.objects.filter(review = review)
	if judgement.exists():
		print "ALREADY EXISTS", judgement[0].judgement
		return
	temp = sent_tokenize(review.desc)
	sentiments = judger(temp)
	judgement = ReviewJudgement(review = review, judgement = json.dumps(sentiments))
	print judgement.judgement
	judgement.save()

@task
def judge_product(product):
	product = Product.objects.get(id = product)
	product_sentiment = {}
	for review in product.review_set.all():
		temp = judge_review(review.id)
		for each in temp:
			if each in product_sentiment:
				product_sentiment[each] = product_sentiment[each][0] + temp[each][0]
				if product_sentiment[each][0] > 0:
					product_sentiment[each][1] = "Positive"
				elif product_sentiment[each][0] < 0:
					product_sentiment[each][1] = "Negative"
				else:
					product_sentiment[each][1] = "Neutral"
			else:
				product_sentiment[each] = temp[each]
	judgement = ProductJudgement(product = product, judgement = json.dumps(product_sentiment))
	judgement.save()