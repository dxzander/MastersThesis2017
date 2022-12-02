import zutil
import sys
import getopt
import math

def term_frequency(term, tokenized_document):
	return tokenized_document.count(term)

def sublinear_term_frequency(term, tokenized_document):
	count = tokenized_document.count(term)
	if count == 0:
		return 0
	return 1 + math.log(count)

#def augmented_term_frequency(term, tokenized_document):
#	max_count = max([term_frequency(t, tokenized_document) for t in tokenized_document])
#	return (0.5 + ((0.5 * term_frequency(term, tokenized_document)) / max_count))

def inverse_document_frequencies(all_texts):
	idf_values = {}
	all_tokens_set = set([item for sublist in all_texts for item in sublist])
	for tkn in all_tokens_set:
		contains_token = map(lambda doc: tkn in doc, all_texts)
		idf_values[tkn] = 1 + math.log(len(all_texts)/(sum(contains_token)))
	return idf_values

def tfidf(documents, idf, histogram):
	#tokenized_documents = [tokenize(d) for d in documents]
	#idf = inverse_document_frequencies(tokenized_documents)
	tfidf_documents = []
	for document in documents:
		doc_tfidf = []
		for term in histogram:
			tf = sublinear_term_frequency(term, document)
			if term in idf.keys():
				doc_tfidf.append(tf * idf[term])
			else:
				doc_tfidf.append(0)
		tfidf_documents.append(doc_tfidf)
	return tfidf_documents

def main(argv):
	# init
	description = 'ztfidf.py-v <var directory>  -t <histogram file> -i <list of input files>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hv:t:i:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-v':
			var_folder = arg + '/'
		elif opt == '-t':
			histogram_file = arg
		elif opt == '-i':
			list_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)
	histogram = zutil.loadUser(histogram_file) #lol hax

	# load and extract all users texts into a single list
	# send them to idf
	# unload all texts from memory
	# reload each user, one by one
	# vectorize their texts using tfidf

	# training and testing modes for idf calculation
	# load and  save idf files

	# idf
	#if "train" in list_file:
	#	users_texts = []
	#	for file in input_files:
	#		user = zutil.loadUser(file)
	#		texts = zutil.getUserTexts(user)
	#		users_texts += texts
	#	idf = inverse_document_frequencies(users_texts)
	#	del users_texts
	#	zutil.saveUser(idf, var_folder + 'idf.pkl') #lol hax
	#else:
	#	idf = zutil.loadUser(var_folder + 'idf.pkl')

	idf = zutil.loadUser(var_folder + 'idf.pkl')

	# process text
	for file in input_files:
		user = zutil.loadUser(file)
		user_texts = zutil.getUserTexts(user)
		texts = tfidf(user_texts, idf, histogram)
		new_user = zutil.saveUserTexts(user, texts)
		zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])
