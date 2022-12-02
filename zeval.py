import zutil
import sys
import getopt

def main(argv):
	# init
	description = 'zeval.py -m <mode> -r <results directory>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:r:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			mode = arg
		elif opt == '-r':
			results_folder = arg + '/'

	# initialize

	

if __name__ == "__main__":
	main(sys.argv[1:])