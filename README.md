# sentientX
Understand the sentiment of user reviews and provide useful information for the end-user as well as the product manufacturer regarding public opinion of the product.

##Setup##
1. Download "stanford-corenlp-full-2015-12-09" from http://stanfordnlp.github.io/CoreNLP/
2. mkdir libs
3. Unzip "stanford-corenlp-full-2015-12-09" and move it to libs/
4. pip install -U nltk
5. virtualenv env --system-site-packages
6. source env/bin/activate
7. pip install -r requirements.txt
8. cd senti
9. ./manage.py runserver
