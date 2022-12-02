import zutil
import sys
import getopt

def saveCSV(data, file, labels = [], separator = ','):
	with open(file, 'w') as f:
		f.write(separator.join(labels) + '\n')
		for element in data:
			f.write(separator.join([str(i) for i in element]) + '\n')
	return 0

def main(argv):
	# init
	description = 'zcsv.py -c <number of chunks> -r <results directory> -i <input file>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:c:r:i:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-c':
			chunk = int(arg)
		elif opt == '-r':
			results_folder = arg + '/'
		elif opt == '-i':
			list_file = arg
		
	# initialize
	input_files = zutil.getUserList(list_file)
	users_data = []
	#labels = ['id', 'pos', 'neg', 'negpos', 'posneg', 'negneg', 'pospos', 'n1', 't1', 'm1', 'n0', 't0', 'm0']
	labels = ['m0', 't0', 'n0', 'm1', 't1', 'n1', 'm2', 't2', 'n2', 'm3', 't3', 'n3', 'm4', 't4', 'n4', 'm5', 't5', 'n5', 'm6', 't6', 'n6']
	users_type = 'test' if 'test' in list_file else 'train'
	if users_type == 'train':
		labels.append('status')
	output_file = results_folder + users_type + '_chunk_' + str(chunk) + '.csv'

	# load data
	print('Loading Training Texts')
	for file in input_files:
		user = zutil.loadUser(file)
		user_texts = zutil.getUserTexts(user)
		user_data = [user['id']] + user_texts[0]
		if users_type == 'train':
			user_data.append(user['status'])
		users_data.append(user_data)

	# save
	saveCSV(users_data, output_file, labels)

if __name__ == "__main__":
	main(sys.argv[1:])