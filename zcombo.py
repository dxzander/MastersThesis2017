import zutil
import sys
import getopt

def main(argv):
	# init
	description = 'zcombo.py -0 <current process directory> -1 <process 1 directory> -2 <process 2 directory> -c <number of chunks>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, 'h0:1:2:c:')
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-0':
			proc0_folder = arg + '/'
		elif opt == '-1':
			proc1_folder = arg + '/'
		elif opt == '-2':
			proc2_folder = arg + '/'
		elif opt == '-c':
			chunk = arg

	# initialize
	proc0_folder = proc0_folder + chunk + '/'
	proc1_folder = proc1_folder + chunk + '/'
	proc2_folder = proc2_folder + chunk + '/'

	proc0_files = zutil.getUserList(proc0_folder + 'var/' + ('train' if chunk == 'train' else 'test') + '.txt')
	proc1_files = zutil.getUserList(proc1_folder + 'var/' + ('train' if chunk == 'train' else 'test') + '.txt')
	proc2_files = zutil.getUserList(proc2_folder + 'var/' + ('train' if chunk == 'train' else 'test') + '.txt')

	# join vectors
	for proc0_file, proc1_file, proc2_file in zip(proc0_files, proc1_files, proc2_files):
		user1 = zutil.loadUser(proc1_file)
		user2 = zutil.loadUser(proc2_file)
		user1_texts = zutil.getUserTexts(user1)
		user2_texts = zutil.getUserTexts(user2)
		user0_texts = [text1 + text2 for text1, text2 in zip(user1_texts, user2_texts)]
		user0 = zutil.saveUserTexts(user1, user0_texts)
		zutil.saveUser(user0, proc0_file)

if __name__ == "__main__":
	main(sys.argv[1:])