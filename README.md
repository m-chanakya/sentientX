# sentientX
Understand the sentiment of user reviews and provide useful information for the end-user as well as the product manufacturer regarding public opinion of the product.

##Setup
Download "stanford-corenlp-full-2015-12-09" from http://stanfordnlp.github.io/CoreNLP/
mkdir libs
Unzip "stanford-corenlp-full-2015-12-09" and move it to libs/
pip install -U nltk
virtualenv env --system-site-packages
source env/bin/activate
pip install -r requirements.txt
cd senti
./manage.py runserver
