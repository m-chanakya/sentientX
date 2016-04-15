"""senti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', 'crawler.views.home', name='home'),

    url(r'crawler/categories', 'crawler.views.categories', name='categories'),
    url(r'crawler/products/(?P<category_id>\w+)', 'crawler.views.products', name='products'),
    url(r'crawler/reviews/(?P<product_id>\w+)/(?P<start>[0-9]+)', 'crawler.views.reviews', name='reviews'),
    url(r'crawler/crawl/(?P<type>\w+)/(?P<id>\w+)', 'crawler.views.crawl', name='crawl'),

    url(r'judge/categories', 'judge.views.categories', name='jcategories'),
    url(r'judge/products/(?P<category_id>\w+)', 'judge.views.products', name='jproducts'),
    url(r'judge/reviews/(?P<product_id>\w+)/(?P<start>[0-9]+)', 'judge.views.reviews', name='jreviews'),
    url(r'judge/judge/(?P<type>\w+)/(?P<id>\w+)', 'judge.views.judge', name='jcrawl'),
    url(r'judge/result/(?P<type>\w+)/(?P<id>\w+)', 'judge.views.results', name='jresults'),
]
