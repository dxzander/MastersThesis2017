### other experiment

# from datetime import datetime, timedelta

# first = datetime(2014, 6, 20, 8, 32, 50)
# last = datetime(2015, 5, 20, 8, 32, 50)

# timespan = abs(first - last)
# print(timespan)

### other experiment

# from sklearn.naive_bayes import MultinomialNB
# from sklearn import datasets
# iris = datasets.load_iris()

# mnb = MultinomialNB()
# y_pred = mnb.fit(iris.data, iris.target).predict_proba(iris.data)
# tags = list(set(iris.target.tolist()))
# probs = y_pred.tolist() 
# results = [list(zip(i, tags)) for i in probs]

### other experiment

# import ztime
# from datetime import datetime, timedelta

# user_times = [datetime(2017, 6, 22, 7, 32, 50), datetime(2017, 6, 23, 8, 32, 50), datetime(2017, 6, 24, 15, 32, 50), datetime(2017, 6, 25, 0, 32, 50)]

# new_user = ztime.sincronizer(user_times)
# print(new_user)

# print(user_times[0].hour)

### other experiment

# import numpy as np
# import random

# a = [[random.random() for x in range(0, 7)] for y in range(0, 24)]
# b = [[random.random() for x in range(0, 7)] for y in range(0, 24)]

# a = [2, 2, 2, 2]
# b = [1, 1, 1, 1]

# coef = np.corrcoef(a, b)[1, 0]

# print(coef)

### other experiment

# import zwam
# import random

# a = [[random.randint(0, 10) for hour in range(5)] for day in range(6)]
# b = [[random.randint(0, 10) for hour in range(5)] for day in range(6)]
# ab = zwam.sumWeekActivities(a, b)

# print(a)
# print(b)
# print(ab)

### other experiment

# a = [0, 0]
# a[0] = 1
# print(a)

### other experiment

# import sys
# sys.path.insert(0, '/home/zander/Dropbox/Maestría/Proyectos/Senticnet')

# import senticnet

### Vector values
# polarity
# attention
# pleasantness
# aptitude
# sensitivity

# scnet = senticnet.Senticnet()
# concepts = scnet.data.keys()
# scores = [0, 0, 0, 0, 0]
# n_concepts = 0

# test_string = 'bad horrible '.split()

# for word in test_string:
# 	if word in concepts:
# 		n_concepts += 1
# 		concept_data = scnet.concept(word)
# 		scores[0] += -1 if concept_data['polarity'] == 'negative' else 1
# 		scores[1] += float(concept_data['sentics']['attention'])
# 		scores[2] += float(concept_data['sentics']['pleasantness'])
# 		scores[3] += float(concept_data['sentics']['aptitude'])
# 		scores[4] += float(concept_data['sentics']['sensitivity'])

# if n_concepts != 0:
# 	scores = [round(score / n_concepts, 4) for score in scores]

# print(scores + [0, 0])

### other experiment

# import zwsa
# from datetime import datetime, timedelta
# import random

# user_times = [datetime(2017, 6, 22, 7, 32, 50), datetime(2017, 6, 23, 8, 32, 50), datetime(2017, 6, 24, 15, 32, 50), datetime(2017, 6, 25, 0, 32, 50)]
# user_texts = [[random.random() for x in range(5)] for y in range(len(user_times))]

# print(user_texts)
# print(user_times)

# labels = zwsa.labelsGenerator()
# histogram = [a for a, b in labels]

# week_activity = zwsa.getWeekActivity(user_texts, user_times, histogram)

# print(week_activity)

### other experiment

# from sklearn.svm import SVC
# from sklearn.model_selection import GridSearchCV
# tuned_parameters = {
# 	'C': [i / 10 for i in range(5, 55, 5)],
# 	'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
# 	'degree': [i for i in range(2, 5)],
# 	'gamma': ['auto'] + [i / 10 for i in range(0, 11)],
# 	'coef0': [i / 10 for i in range(0, 11)],
# 	'shrinking': [True, False],
# 	'max_iter': [-1] + [i for i in range(10, 110, 10)],
# 	'random_state': [None] + [i for i in range(1, 11)],
# 	}
# classifier = GridSearchCV(SVC(), tuned_parameters, cv = 5)

### other experiment

# import zutil

# time_train_file = '/home/zander/Desktop/time/train/tmp/train_subject1015.pkl'
# week_train_file = '/home/zander/Desktop/weekly/train/tmp/train_subject1015.pkl'
# time_test_file = '/home/zander/Desktop/time/1/tmp/test_subject1005.pkl'
# week_test_file = '/home/zander/Desktop/weekly/1/tmp/test_subject1005.pkl'

# time_train_user = zutil.loadUser(time_train_file)
# week_train_user = zutil.loadUser(week_train_file)
# time_test_user = zutil.loadUser(time_test_file)
# week_test_user = zutil.loadUser(week_test_file)

# print("Time Train User")
# print(time_train_user)
# print("Week Train User")
# print(week_train_user)
# print("Time Test User")
# print(time_test_user)
# print("Week Test User")
# print(week_test_user)

### other experiment

import zutil
import re
from nltk import regexp_tokenize

test_urls = ['https://docs.python.org/3/library/re.html', 'http://wikitable2csv.ggor.de/', 'https://en.wikipedia.org/wiki/List_of_Internet_top-level_domains#Country_code_top-level_domains', 'https://stackoverflow.com/questions/569137/how-to-get-domain-name-from-url']
sample_text = """French involvement in [2011 Libyan War](http://en.wikipedia.org/wiki/2011_military_intervention_in_Libya)

French involvement in [current Syrian War](http://en.wikipedia.org/wiki/Foreign_involvement_in_the_Syrian_Civil_War)

French involvement in [current war on ISIS](http://www.nytimes.com/2014/09/19/world/europe/leader-vows-french-role-in-airstrikes-on-isis-in-iraq.html?_r=0)

French involvement in [current wars in Mali and elsewhere in Africa](http://www.newsweek.com/2014/11/07/france-slowly-reclaiming-its-old-african-empire-280635.html)

When governments engage in mass murder around the globe, the victims or their sympathizers will inevitably retaliate against the perceived aggressor.  Even a self-described "conservative" should be able to understand that logic."""

# for url in test_urls:
# 	site = zutil.removeURLs(url)
# 	print(site)

# url_pattern = r'\(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\)'
# urls = re.findall(url_pattern, sample_text)
# print(urls)
# domains = [url.split('/')[2].replace('www.', '').replace('.', '-') for url in urls]
# new_text = sample_text
# for url, domain in zip(urls, domains):
# 	new_text = new_text.replace(url, domain)

new_text = zutil.simplifyURLs(sample_text)

new_text = regexp_tokenize(new_text, r'[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]+-*[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]+-*[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]*|[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]+|[.]+|[/,$?:;!()&%#=+{}*~.]+')
print(new_text)