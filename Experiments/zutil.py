import sys
import os.path
import pickle
import re
from nltk import regexp_tokenize
from collections import Counter
import math

def getDataFolder(var_folder):
	with open(var_folder + 'data.txt', 'r') as f:
		data_folder = f.read().replace('\n', '/')
	return data_folder

def saveFileList(filename, files):
	with open(filename, 'w') as f:
		for file in files:
			f.write(file + '\n')

def getUserList(list_file):
	with open(list_file, 'r') as f:
		users = f.readlines()
		users = [x.strip() for x in users]
	return users

def getOutputFile(user, files):
	output_file = [file for file in files if user + '.pkl' in file]
	output_file = output_file[0]
	return output_file

def saveUser(user, user_file):
	with open(user_file, 'wb') as f:
		pickle.dump(user, f)

def loadUser(user_file):
	with open(user_file, 'rb') as f:
		user = pickle.load(f)
	return user

def getUserTexts(user):
	texts = [post['text'] for post in user['posts']]
	return texts

def getUserTimes(user):
	times = [post['date'] for post in user['posts']]
	return times

def saveUserTexts(user, texts):
	for post in range(len(texts)):
		user['posts'][post]['text'] = texts[post]
	return user

def saveUserNewRepresentation(user, texts):
	user['posts'] = []
	for text in texts:
		user['posts'] += [{'text': text}]
	return user

def joinNegations(text):
	new_text = []
	neg_words = ['no', 'not', 'never', 'bad', 'don\'t', 'doesn\'t', 'didn\'', 'won\'t', 'can\'t', 'wouldn\'t', 'couldn\'t', 'isn\'t', 'ain\'t', 'aren\'t', 'dont', 'doesnt', 'didnt', 'wont', 'cant','wouldnt', 'couldnt', 'isnt', 'aint', 'arent']
	for word in range(len(text)):
		if word == 0:
			if text[word] in neg_words:
				continue
			else:
				new_text.append(text[word])
		elif word < len(text) - 1:
			if text[word] in neg_words:
				new_text.append('_'.join([text[word], text[word + 1]]))
			else:
				if text[word - 1] in neg_words:
					continue
				else:
					new_text.append(text[word])
		elif word == len(text) - 1:
			if text[word - 1] in neg_words:
				continue
			else:
				new_text.append(text[word])
	return new_text

def createNgrams(text, number):
	ngrams = ['_'.join(text[word:word + number]) for word in range(len(text) - number + 1)]
	return ngrams

def simplifyURLs(text):
	url_pattern = r'[\(]?http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+[\)]?'
	urls = re.findall(url_pattern, text)
	domains = [url.split('/')[2].replace('www.', '').replace('.', '-') for url in urls]
	for url, domain in zip(urls, domains):
		text = text.replace(url, domain)
	text = text.replace('https', '').replace('http', '').replace('htt', '')
	return text

def stdDepPipeline(text, ngram):
	# remove new lines
	text = text.replace('\n', ' ')
	# remove numbers
	# text = re.sub(r'[\d]+', '', text)
	# remove uppercase
	# text = text.lower()
	# simplify urls
	# text = simplifyURLs(text)
	# tokenize
	text = regexp_tokenize(text, r'[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]+-*[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]+-*[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]*|[a-zA-Z\'ÁÉÍÓÚáéíóúñÑüÜ]+|[.]+|[/,$?:;!()&%#=+{}*~.]+|[\d]+')
	# join negations
	# text = joinNegations(text)
	# ngram management
	if ngram == 0:
		bigrams = createNgrams(text, 2)
		trigrams = createNgrams(text, 3)
		text += bigrams + trigrams
	elif ngram == 1:
		return text
	else:
		text = createNgrams(text, ngram)
	return text

def wordCounterInit():
	word_counts = Counter()
	return word_counts

def wordCounterFull(texts):
	# to convert to how many times at all, remove the set()
	# to convert to how many documents feature them,
	# enclose text in update within set()
	word_counts = Counter()
	for text in texts:
		word_counts.update(text)
	return word_counts

def wordCounterPartial(word_counts, texts):
	for text in texts:
		word_counts.update(text)
	return word_counts

def timeData(time):
	hour = time.hour
	day = 0 if time.weekday() < 5 else 1
	time = [hour] + [day]
	return time

def vainillaVectorizer(text, vector):
	text_counts = Counter(text)
	# no normalization
	text = [text_counts[element] for element in vector]

	# normalization
	# total_words = len(text)
	# if total_words != 0:
	# 	text = [text_counts[element] / total_words for element in vector]
	# else:
	# 	text = [text_counts[element] for element in vector]
	return text

def timeVectorizer(text, time, vector):
	bow = vainillaVectorizer(text, vector)
	time = timeData(time)
	text = bow + time
	return text

def sentiVectorizer(text, time, vector):
	import zsenti
	bow = vainillaVectorizer(text, vector)
	senti = zsenti.sentimentAnalyzerFull(text)
	time = timeData(time)
	text = bow + senti + time
	return text

def sumVectors(x1, x2):
	x3 = [a + b for a, b in zip(x1, x2)]
	return x3
