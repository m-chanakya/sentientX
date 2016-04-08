from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=100)
	sid = models.CharField(max_length=10)
	link = models.URLField()
	crawled_date = models.DateTimeField(auto_now_add=True)
	total = models.SmallIntegerField(default = 1500)

class Product(models.Model):
	name = models.CharField(max_length=100)
	link = models.URLField()
	category = models.ForeignKey(Category)
	crawled_date = models.DateTimeField(auto_now_add=True)
	total = models.SmallIntegerField(default = 0)

class Review(models.Model):
	crawled_date = models.DateTimeField(auto_now_add=True)
	review_id = models.CharField(max_length=100)
	product = models.ForeignKey(Product)
	author = models.CharField(max_length=50)
	certified_buyer = models.BooleanField(default=False)
	review_date = models.DateTimeField()
	product_rating = models.PositiveSmallIntegerField()
	title = models.CharField(max_length=200)
	desc = models.TextField()
	upvotes = models.PositiveSmallIntegerField()
	total_votes = models.PositiveSmallIntegerField()