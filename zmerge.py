import zutil
import sys
import getopt

def main(argv):
	# init
	description = 'zmerge.py -v <var directory> -t <histogram file>'
	histogram_file = False

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hv:t:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-v':
			var_folder = arg + '/'
			if not histogram_file:
				histogram_file = var_folder + 'histogram.pkl'
		elif opt == '-t':
			histogram_file = arg

	# initialize
	ngrams = ['1', '2', '3']
	histogram = []

	# load and merge histograms
	for ngram in ngrams:
		loaded_histogram = zutil.loadUser(var_folder + 'histogram' + ngram + '.pkl') #lol hax
		histogram.extend(loaded_histogram)
	print(str(len(histogram)) + ' total elements in histogram!')

	# save
	zutil.saveUser(histogram, histogram_file) #lol hax

if __name__ == "__main__":
	main(sys.argv[1:])