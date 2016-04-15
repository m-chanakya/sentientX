from __future__ import unicode_literals

from django.db import models
from crawler.models import *

# Create your models here.
class ProductJudgement(models.Model):
	product = models.ForeignKey(Product)
	judgement = models.TextField()

class ReviewJudgement(models.Model):
	review = models.ForeignKey(Review)
	judgement = models.TextField()