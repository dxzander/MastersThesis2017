import zutil
import sys
import getopt

def main(argv):
	# init
	description = 'zcount.py -v <var directory> -r <results directory> -m <mode: combo|class> -g <number of ngrams> -n <max terms: 0|-1|number> -i <list of input files>'
	max_counts = 10000
	ngrams = 0
	mode = 'combo'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hv:r:g:m:n:i:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-v':
			var_folder = arg + '/'
		elif opt == '-r':
			results_folder = arg + '/'
		elif opt == '-g':
			ngrams = arg
		elif opt == '-m':
			if arg == 'combo' or arg == 'class':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-n':
			max_counts = int(arg)
		elif opt == '-i':
			list_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)
	word_counts = zutil.wordCounterInit()
	pos_counts = zutil.wordCounterInit()
	neg_counts = zutil.wordCounterInit()

	if mode == 'class':
		# count words
		for file in input_files:
			user = zutil.loadUser(file)
			user_texts = zutil.getUserTexts(user)
			if user['status'] == 1:
				pos_counts = zutil.wordCounterPartial(pos_counts, user_texts)
			elif user['status'] == 0:
				neg_counts = zutil.wordCounterPartial(neg_counts, user_texts)
		n_pos = len(pos_counts)
		n_neg = len(neg_counts)

		if max_counts == 0:
			n_pos = round(n_pos / 5)
			n_neg = round(n_neg / 5)
			pos_histogram = [element for (element, count) in pos_counts.most_common(n_pos)]
			neg_histogram = [element for (element, count) in neg_counts.most_common(n_neg)]

			pos_data = [pair for pair in pos_counts.most_common(n_pos)]
			neg_data = [pair for pair in neg_counts.most_common(n_neg)]

			n_pos = len(pos_counts)
			n_neg = len(neg_counts)
		elif max_counts == -1:
			pos_histogram = [element for (element, count) in pos_counts.most_common() if count > 1]
			neg_histogram = [element for (element, count) in neg_counts.most_common() if count > 1]

			pos_data = [pair for pair in pos_counts.most_common() if pair[1] > 1]
			neg_data = [pair for pair in neg_counts.most_common() if pair[1] > 1]
		else:
			pos_histogram = [element for (element, count) in pos_counts.most_common(max_counts)]
			neg_histogram = [element for (element, count) in neg_counts.most_common(max_counts)]

			pos_data = [pair for pair in pos_counts.most_common(max_counts)]
			neg_data = [pair for pair in neg_counts.most_common(max_counts)]

		# save file
		zutil.saveUser(pos_histogram, var_folder + 'pos_histogram' + ngrams + '.pkl') #lol hax
		zutil.saveUser(neg_histogram, var_folder + 'neg_histogram' + ngrams + '.pkl') #lol hax

		with open(results_folder + 'histogram_pos.csv', 'w') as f:
			f.write('total' + '\t' + str(n_pos) + '\n')
			for pair in pos_data:
				f.write('\t'.join(str(x) for x in pair) + '\n')

		with open(results_folder + 'histogram_neg.csv', 'w') as f:
			f.write('total' + '\t' + str(n_neg) + '\n')
			for pair in neg_data:
				f.write('\t'.join(str(x) for x in pair) + '\n')

	elif mode == 'combo':
		# count words
		for file in input_files:
			user = zutil.loadUser(file)
			user_texts = zutil.getUserTexts(user)
			word_counts = zutil.wordCounterPartial(word_counts, user_texts)
		n_words = len(word_counts)

		if max_counts == 0:
			n_words = round(n_words / 5)
			histogram = [element for (element, count) in word_counts.most_common(n_words)]
		elif max_counts == -1:
			histogram = [element for (element, count) in word_counts.most_common() if count > 1]
		else:
			histogram = [element for (element, count) in word_counts.most_common(max_counts)]

		# save file
		zutil.saveUser(histogram, var_folder + 'histogram' + ngrams + '.pkl') #lol hax

if __name__ == "__main__":
	main(sys.argv[1:])