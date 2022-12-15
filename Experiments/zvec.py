import zutil
import sys
import getopt

def textVectorization(user, histogram, mode):
	texts = zutil.getUserTexts(user)
	if mode == 'user':
		texts = [zutil.vainillaVectorizer(text, histogram) for text in texts]
	elif mode == 'post':
		times = zutil.getUserTimes(user)
		texts = [zutil.timeVectorizer(text, time, histogram) for text, time in zip(texts, times)]
	elif mode == 'senti':
		times = zutil.getUserTimes(user)
		texts = [zutil.sentiVectorizer(text, time, histogram) for text, time in zip(texts, times)]
	new_user = zutil.saveUserTexts(user, texts)
	return new_user

def main(argv):
	# init
	description = 'zvec.py -m <mode: user|post|senti> -t <histogram file> -i <list of input files>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:t:i:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			if arg == 'user' or arg == 'post' or arg == 'senti':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-t':
			histogram_file = arg
		elif opt == '-i':
			list_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)
	histogram = zutil.loadUser(histogram_file) #lol hax

	# process text
	for file in input_files:
		user = zutil.loadUser(file)
		new_user = textVectorization(user, histogram, mode)
		zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])