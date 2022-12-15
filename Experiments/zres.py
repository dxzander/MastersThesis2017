import zutil
import sys
import getopt

def main(argv):
	# init
	description = 'zres.py -i <input file> -o <results file>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hi:o:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-i':
			list_file = arg
		elif opt == '-o':
			results_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)

	# process text
	with open(results_file, 'w') as f:
		for file in input_files:
			user = zutil.loadUser(file)
			f.write(user['id'] + '\t\t' + str(user['posts'][0]['text']) + '\n')

if __name__ == "__main__":
	main(sys.argv[1:])
