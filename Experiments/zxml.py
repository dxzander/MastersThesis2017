import zutil
import sys
import getopt
from os import listdir
import xmldict
from datetime import datetime

'''
Original structure
Each user has:
	-INDIVIDUAL
		- ID
		- STATUS
		- WRITING
			- TEXT
			- DATE
			- INFO
			- TITLE

Statuses:
0 for not depressed, 1 for depressed
'''

'''
New structure
Each user has:
	- id
	- status
	- posts
		- text (title + text)
		- date
Statuses:
0 for not depressed, 1 for depressed
'''

def structurize(user):
	posts = []
	if type(user['INDIVIDUAL']['WRITING']) is list:
		for write in range(len(user['INDIVIDUAL']['WRITING'])):
			post = {
				'text': user['INDIVIDUAL']['WRITING'][write]['TITLE'] + ' ' + user['INDIVIDUAL']['WRITING'][write]['TEXT'],
				'date': datetime.strptime(user['INDIVIDUAL']['WRITING'][write]['DATE'], '%Y-%m-%d %H:%M:%S'),
			}
			posts.append(post)
		posts = list(reversed(posts))
		new_user = {
			'id': user['INDIVIDUAL']['ID'],
			'posts': posts
		}
	elif type(user['INDIVIDUAL']['WRITING']) is dict:
		post = {
			'text': user['INDIVIDUAL']['WRITING']['TITLE'] + ' ' + user['INDIVIDUAL']['WRITING']['TEXT'],
			'date': datetime.strptime(user['INDIVIDUAL']['WRITING']['DATE'], '%Y-%m-%d %H:%M:%S'),
		}
		new_user = {
			'id': user['INDIVIDUAL']['ID'],
			'posts': [post]
		}
	return new_user

def mergeUserPosts(user):
	posts = {
		'text': ' '.join(zutil.getUserTexts(user))
	}
	if 'status' in user:
		new_user = {
			'id': user['id'],
			'status': user['status'],
			'posts': [posts]
		}
	else:
		new_user = {
			'id': user['id'],
			'posts': [posts]
		}
	return new_user

def textProcessing(user, ngrams):
	texts = zutil.getUserTexts(user)
	texts = [zutil.stdDepPipeline(text, ngrams) for text in texts]
	new_user = zutil.saveUserTexts(user, texts)
	return new_user

def createDateStructure():
	structure = {year: {month: 0 for month in range(1, 13)} for year in range(5, 17)}
	return structure

def main(argv):
	# init
	description = 'zxml.py -m <mode: user|post> -g <number of ngrams> -c <number of chunks> -i <list of input files> -o <output folder> -f <filtering? y|n>'
	ngrams = 0
	filtering = False

	# get input argument
	try:
		opts, args = getopt.getopt(argv, 'hm:g:c:i:o:f:')
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			if arg == 'user' or arg == 'post':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-g':
			ngrams = int(arg)
		elif opt == '-c':
			chunk = int(arg)
		elif opt == '-i':
			output_files = arg
		elif opt == '-o':
			tmp_folder = arg + '/'
		elif opt == '-f':
			if arg == 'y':
				filtering = True

	# initialize
	var_folder = tmp_folder.replace('tmp', 'var')
	data_folder = zutil.getDataFolder(var_folder)
	outputs = zutil.getUserList(output_files)
	neg_folder = data_folder + 'negative_examples_anonymous/'
	pos_folder = data_folder + 'positive_examples_anonymous/'

	if 'train' in output_files:
		# get training files
		neg_file = [neg_folder + file for file in listdir(neg_folder)]
		pos_file = [pos_folder + file for file in listdir(pos_folder)]
		training_files = neg_file + pos_file

		# initialize data counts
		pos_date_data = createDateStructure()
		neg_date_data = createDateStructure()

		# load training files
		for file in training_files:
			with open(file, 'r') as f:
				data = f.read()
				user = xmldict.xml_to_dict(data)
				new_user = structurize(user)
				if 'positive' in file:
					new_user['status'] = 1
				elif 'negative' in file:
					new_user['status'] = 0
				for post in new_user['posts']:
					date = post['date']
					year = date.year - 2000
					month = date.month
					if new_user['status'] == 1:
						pos_date_data[year][month] += 1
					else:
						neg_date_data[year][month] += 1
				if mode == 'user':
					new_user = mergeUserPosts(new_user)
				new_user = textProcessing(new_user, ngrams)
				output_file = zutil.getOutputFile(new_user['id'], outputs)
				if filtering:
					tmp_user = new_user
					filtered_user = zutil.loadUser(output_file.replace('.pkl', '_fil.pkl'))
					filtered_texts = zutil.getUserTexts(filtered_user)
					normal_texts = zutil.getUserTexts(tmp_user)
					new_texts = [post for post, status in zip(normal_texts, filtered_texts) if status == new_user['status']]
					new_user = zutil.saveUserTexts(tmp_user, new_texts)
				zutil.saveUser(new_user, output_file)

		# save dates data
		results_folder = '/home/zander/ownCloud/Maestría/Proyectos/depression reddit/results/' #lol lazy
		pos_date_file = results_folder + 'results_dates_pos.csv'
		neg_date_file = results_folder + 'results_dates_neg.csv'
		date_files = [pos_date_file, neg_date_file]
		date_data = [pos_date_data, neg_date_data]
		months = {
			1: 'Enero',
			2: 'Febrero',
			3: 'Marzo',
			4: 'Abril',
			5: 'Mayo',
			6: 'Junio',
			7: 'Julio',
			8: 'Agosto',
			9: 'Septiembre',
			10: 'Octubre',
			11: 'Noviembre',
			12: 'Diciembre'
		}

		for file, data in zip(date_files, date_data):
			with open(file, 'w') as f:
				for year in range(5, 17):
					for month in range(1, 13):
						f.write(months[month] + '_' + str(2000 + year) + ',' + str(data[year][month]) + '\n')

	elif 'test' in output_files:
		# get testing files
		testing_chunks = listdir(data_folder + 'testing/')
		testing_chunks.sort()
		testing_chunks = testing_chunks[:chunk]
		testing_files = []
		for chunk_folder in testing_chunks:
			chunk_files = listdir(data_folder + 'testing/' + chunk_folder + '/')
			chunk_files.sort()
			chunk_files = [data_folder + 'testing/' + chunk_folder + '/' + file for file in chunk_files]
			testing_files.append(chunk_files)
		
		# load testing files
		for user_files in zip(*testing_files):
			user_posts = []
			for file in user_files:
				with open(file, 'r') as f:
					data = f.read()
					user = xmldict.xml_to_dict(data)
					partial_user = structurize(user)
					# Original procedure
					# partial_user = textProcessing(partial_user, ngrams)
				user_id = partial_user['id']
				user_posts += partial_user['posts']
			new_user = {
				'id': user_id,
				'posts': user_posts
			}
			# new procedure
			if mode == 'user': # part of the new
				new_user = mergeUserPosts(new_user) # part of the new
			new_user = textProcessing(new_user, ngrams) # part of the new
			output_file = zutil.getOutputFile(new_user['id'], outputs)
			zutil.saveUser(new_user, output_file)

if __name__ == "__main__":
	main(sys.argv[1:])