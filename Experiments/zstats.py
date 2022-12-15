import zutil
import zxml
import zdec
import sys
import getopt
from os import listdir
from datetime import datetime, timedelta
import xmldict
from operator import itemgetter
from sklearn.metrics import classification_report

def main(argv):
	# init
	description = 'zstats.py -m <mode> -p <probabilities? y|n>'
	p = 'y'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:p:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		if opt == '-m':
			mode = arg
		if opt == '-p':
			p = arg

	# initialize
	chunks = 10
	testing_truth = '/home/zander/ownCloud/Maestría/Datasets/reddit-depression/test_golden_truth.txt'
	results_folder = '/home/zander/ownCloud/Maestría/Proyectos/depression reddit/results/'  #lol lazy
	data_folder = '/home/zander/ownCloud/Maestría/Datasets/reddit-depression/'
	results_file = results_folder + 'results_study.csv'
	fscores_file = results_folder + 'results_fscores.txt'
	mode_proba = mode.replace('nbc', 'nbc_proba')
	decisions_file = results_folder + 'test_users_decisions.csv'
	decisions_files = ['CHEPEA_10.txt', 'CHEPEB_10.txt', 'CHEPEC_10.txt', 'CHEPED_10.txt']
	target_names = ['not depressed', 'depressed']

	# get testing files
	testing_chunks = listdir(data_folder + 'testing/')
	testing_chunks.sort()
	testing_chunks = testing_chunks[:chunks]
	testing_files = []
	for chunk_folder in testing_chunks:
		chunk_files = listdir(data_folder + 'testing/' + chunk_folder + '/')
		chunk_files.sort()
		chunk_files = [data_folder + 'testing/' + chunk_folder + '/' + file for file in chunk_files]
		testing_files.append(chunk_files)

	# get testing classes
	users_classes = zutil.getUserList(testing_truth)
	users_classes = [user.split() for user in users_classes]
	users_classes = sorted(users_classes, key = itemgetter(0))
	real_classes = [int(user[1]) for user in users_classes]

	# get results
	fscores = []
	for chunk in range(1, chunks + 1):
		predictions = zdec.getUserPredictions(results_folder + mode + '_' + str(chunk) + '.txt')
		prediction_classes = [int(prediction['predictions'][0]) for prediction in predictions]
		fscores.append('Chunk ' + str(chunk))
		fscores.append(classification_report(prediction_classes, real_classes, target_names = target_names, digits = 4))
		if chunk == 1:
			users_results = predictions
		else:
			users_results = zdec.mergeUserPredictions(users_results, predictions)

	# get probabilities
	if p == 'y':
		for chunk in range(1, chunks + 1):
			predictions = zdec.getUserPredictions(results_folder + mode_proba + '_' + str(chunk) + '.txt')
			if chunk == 1:
				users_proba = predictions
			else:
				users_proba = zdec.mergeUserPredictions(users_proba, predictions)
	
	# get user's stats
	users_stats = []

	for user_files in zip(*testing_files):
		user_posts = []
		for file in user_files:
			with open(file, 'r') as f:
				data = f.read()
				user = xmldict.xml_to_dict(data)
				partial_user = zxml.structurize(user)
			user_id = partial_user['id']
			user_posts += partial_user['posts']
		new_user = {
			'id': user_id,
			'posts': user_posts
		}
		new_user['num_posts'] = len(new_user['posts'])
		new_user['time_span'] = abs(new_user['posts'][0]['date'] - new_user['posts'][-1]['date'])
		new_user['time_span'] = new_user['time_span'] / timedelta(days = 1)
		new_user.pop('posts')
		users_stats.append(new_user)
	users_stats = sorted(users_stats, key = lambda k: k['id'])

	# get all decisions from master decision file
	# decisions = zdec.getUserPredictions(results_folder + file)
	# decision_classes = [int(decision['predictions'][0]) for decision in decisions]
	# decision_classes = [1 if decision == 1 else 0 for decision in decision_classes]
	# fscores.append(str(file))
	# fscores.append(classification_report(decision_classes, real_classes, target_names = target_names, digits = 4))
	# if file == 'CHEPEA_10.txt':
	# 	users_decisions = decisions
	# else:
	# 	users_decisions = zdec.mergeUserPredictions(users_decisions, decisions)

	# get decisions from contest decision files
	for file in decisions_files:
		decisions = zdec.getUserPredictions(results_folder + file)
		decision_classes = [int(decision['predictions'][0]) for decision in decisions]
		decision_classes = [1 if decision == 1 else 0 for decision in decision_classes]
		fscores.append(str(file))
		fscores.append(classification_report(real_classes, decision_classes, target_names = target_names, digits = 4))
		if file == 'CHEPEA_10.txt':
			users_decisions = decisions
		else:
			users_decisions = zdec.mergeUserPredictions(users_decisions, decisions)
	
	# save data
	if p == 'y':
		with open(results_file, 'w') as f:
			f.write('User ID\tStatus\tNumber of Posts\tTime Span\tPrediction 1 chunk\tPrediction 2 chunk\tPrediction 3 chunk\tPrediction 4 chunk\tPrediction 5 chunk\tPrediction 6 chunk\tPrediction 7 chunk\tPrediction 8 chunk\tPrediction 9 chunk\tPrediction 10 chunk\tProbability 1 chunk\tProbability 2 chunk\tProbability 3 chunk\tProbability 4 chunk\tProbability 5 chunk\tProbability 6 chunk\tProbability 7 chunk\tProbability 8 chunk\tProbability 9 chunk\tProbability 10 chunk\tLast 3\tLast 5\tFirst 3\tFirst 5\t\n')
			for user in zip(users_classes, users_stats, users_results, users_proba, users_decisions):
				decisions = ['1' if prediction == '1' else '0' for prediction in user[4]['predictions']]
				f.write(user[1]['id'] + '\t' + str(user[0][1]) + '\t' + str(user[1]['num_posts']) + '\t' + str(user[1]['time_span']) + '\t' + '\t'.join(user[2]['predictions'])+ '\t' + '\t'.join(user[3]['predictions']) + '\t' + '\t'.join(decisions) + '\n')
	elif p == 'n':
		with open(results_file, 'w') as f:
			f.write('User ID\tStatus\tNumber of Posts\tTime Span\tPrediction 1 chunk\tPrediction 2 chunk\tPrediction 3 chunk\tPrediction 4 chunk\tPrediction 5 chunk\tPrediction 6 chunk\tPrediction 7 chunk\tPrediction 8 chunk\tPrediction 9 chunk\tPrediction 10 chunk\tLast 3\tLast 5\tFirst 3\tFirst 5\t\n')
			for user in zip(users_classes, users_stats, users_results, users_decisions):
				decisions = ['1' if prediction == '1' else '0' for prediction in user[3]['predictions']]
				f.write(user[1]['id'] + '\t' + str(user[0][1]) + '\t' + str(user[1]['num_posts']) + '\t' + str(user[1]['time_span']) + '\t' + '\t'.join(user[2]['predictions'])+ '\t' + '\t'.join(decisions) + '\n')

	with open(fscores_file, 'w') as f:
		f.write('\n'.join(fscores))

if __name__ == "__main__":
	main(sys.argv[1:])
