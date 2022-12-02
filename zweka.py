import zutil
import sys
import getopt
import re

def main(argv):
	# init
	description = 'zweka.py -m <mode: export|import> -c <number of chunks> -r <results directory> -t <histogram file> -w <arff file> -i <list of input files> -o <output folder>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:c:r:t:w:i:o:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			if arg == 'export' or arg == 'import':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-c':
			chunk = arg
		elif opt == '-r':
			results_folder = arg + '/'
		elif opt == '-t':
			histogram_file = arg
		elif opt == '-w':
			weka_file = arg
		elif opt == '-i':
			list_file = arg
		elif opt == '-o':
			tmp_folder = arg + '/'

	# initialize
	histogram = zutil.loadUser(histogram_file) # lol hax

	if mode == 'export':
		# export mode

		# initialize
		input_files = zutil.getUserList(list_file)
		classes = {
			0: 'control',
			1: 'depressed'
		}

		# create file
		with open(weka_file, 'w') as f:
			# file header
			f.write('@RELATION depression_posts' + '\n')
			f.write('\n')
			for attribute in range(len(histogram)):
				f.write('@ATTRIBUTE attr' + str(attribute) + ' NUMERIC %' + histogram[attribute] + '\n')
			f.write('@ATTRIBUTE class {' + ','.join([classes[0], classes[1]])  + '}\n')
			f.write('@DATA' + '\n')

			# data section
			for file in input_files:
				user = zutil.loadUser(file)
				for post in user['posts']:
					f.write(','.join(str(x) for x in post['text']) + ',' + str(classes[user['status']]) + '\n')
	
	else:
		# import mode

		#initialize
		attributes = []
		if 'histogram' in histogram_file:
			results_file = results_folder + 'words' + chunk + '.txt'
		else:
			results_file = results_folder + 'tokens' + chunk + '.txt'

		# read file
		with open(weka_file, 'r') as f:
			for line in f:
				if '@data' in line:
					continue
				else:
					text = line.split()
					attribute = [word for word in text if re.match(r'attr[0-9]', word)]
					if attribute:
						attribute = int(attribute[0].replace('attr', ''))
						attributes.append(attribute)

		histogram = [histogram[attribute] for attribute in attributes]
		print('Elements imported: ' + str(len(histogram)))

		# save
		zutil.saveUser(histogram, histogram_file) #lol hax
		with open(results_file, 'w') as f:
			for word in histogram:
				f.write(word + '\n')
				

if __name__ == "__main__":
	main(sys.argv[1:])