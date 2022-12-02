import zutil
import sys
import getopt
from os import listdir
import random

def main(argv):
	# init
	description = 'zinit.py -v <var directory> -c <number of chunks> -i <training file> -o <testing file>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, 'hv:c:i:o:')
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-v':
			var_folder = arg + '/'
		elif opt == '-c':
			chunk = int(arg)
		elif opt == '-i':
			train_file = arg
		elif opt == '-o':
			test_file = arg

	# initialize
	tmp_folder = var_folder.replace('var', 'tmp')
	data_folder = zutil.getDataFolder(var_folder)
	neg_folder = data_folder + 'training/negative_examples_anonymous_chunks/chunk_1/'
	pos_folder = data_folder + 'training/positive_examples_anonymous_chunks/chunk_1/'

	# training files
	neg_file = [tmp_folder + file.replace('_1.xml', '.pkl') for file in listdir(neg_folder)]
	pos_file = [tmp_folder + file.replace('_1.xml', '.pkl') for file in listdir(pos_folder)]
	training_files = neg_file + pos_file

	# testing files
	testing_files = [tmp_folder + file.replace('_1.xml', '.pkl') for file in listdir(data_folder + 'testing/chunk_1/')]

	# shuffle
	# random.shuffle(training_files)
	# random.shuffle(testing_files)

	# sort
	training_files = sorted(training_files)
	testing_files = sorted(testing_files)

	# save to files
	zutil.saveFileList(train_file, training_files)
	zutil.saveFileList(test_file, testing_files)

if __name__ == "__main__":
	main(sys.argv[1:])