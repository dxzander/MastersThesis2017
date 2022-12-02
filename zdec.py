import zutil
import sys
import getopt

def getUserPredictions(results_file):
	with open(results_file, 'r') as f:
		users = f.readlines()
		users = [x.split() for x in users]
		users = [{'id': user[0], 'predictions': [user[1]]} for user in users]
		predictions = sorted(users, key = lambda k: k['id'])
	return predictions

def mergeUserPredictions(users, predictions):
	new_users = [{'id': users[user]['id'], 'predictions': users[user]['predictions'] + predictions[user]['predictions']} for user in range(len(users)) if users[user]['id'] == predictions[user]['id']]
	return new_users

def atLeast(users, number):
	new_users = []
	for user in users:
		n_pos = user['predictions'].count('1')
		new_user = {'id': user['id']}
		if n_pos >= number:
			new_user['prediction'] = '1'
		else:
			new_user['prediction'] = '0'
		new_users.append(new_user)
	return new_users

def mostCommon(users, number):
	# negative number: last x
	# positive number: first x
	# 0: all
	new_users = []
	for user in users:
		if number > 0:
			predictions = user['predictions'][:number]
		elif number < 0:
			predictions = user['predictions'][number:]
		else:
			predictions = user['predictions']
		n_neg = predictions.count('0')
		n_pos = predictions.count('1')
		new_user = {'id': user['id']}
		if n_pos > n_neg:
			new_user['prediction'] = '1'
		else:
			new_user['prediction'] = '0'
		new_users.append(new_user)
	return new_users

def noChanges(users, number):
	new_users = []
	number = -number
	for user in users:
		predictions = user['predictions'][number:]
		n_neg = predictions.count('0')
		n_pos = predictions.count('1')
		new_user = {'id': user['id']}
		if n_pos == 0 or n_neg == 0:
			if n_pos == 0:
				new_user['prediction'] = '0'
			else:
				new_user['prediction'] = '1'
		else:
			new_user['prediction'] = '2'
		new_users.append(new_user)
	return new_users

def main(argv):
	# init
	description = 'zdec.py -m <mode> -c <number of chunks> -r <results directory>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:c:r:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			mode = arg
		elif opt == '-c':
			chunks = int(arg)
		elif opt == '-r':
			results_folder = arg + '/'

	# initialize

	# consolidate users results
	for chunk in range(1, chunks + 1):
		predictions = getUserPredictions(results_folder + mode + '_' + str(chunk) + '.txt')
		if chunk == 1:
			users = predictions
		else:
			users = mergeUserPredictions(users, predictions)

	# save user data
	with open(results_folder + 'test_users_predictions.csv', 'w') as f:
		for user in users:
			f.write(user['id'] + ',' + ','.join(user['predictions']) + '\n')

	# decision schemes

	'''
	- at least two depressive
	- most common in last 3
	- most common in last 5
	- most common overall
	- most common in first 5
	- most common in first 3
	- no changes in last 3, undecided otherwise
	- no changes in last 5, undecided otherwise
	'''

	at_least_two = atLeast(users, 2)
	last_3 = mostCommon(users, -3)
	last_5 = mostCommon(users, -5)
	overall = mostCommon(users, 0)
	first_5 = mostCommon(users, 5)
	first_3 = mostCommon(users, 3)
	no_changes_3 = noChanges(users, 3)
	no_changes_5 = noChanges(users, 5)

	# statistics
	n_users = len(users)
	decisions = [at_least_two, last_3, last_5, overall, first_5, first_3, no_changes_3, no_changes_5]
	statistics = [('Depressed', 'Not Depressed', 'Skip Decision')]

	# save decision data
	with open(results_folder + 'test_users_decisions.csv', 'w') as f:
		f.write('ID, At least two depressive, Most Common in Last 3, Most Common in Last 5, Most Common Overall, Most Common in First 5, Most Common in First 3, No Changes in Last 3, No Changes in Last 5\n')
		for user in zip(*decisions):
			f.write(user[0]['id'])
			for decision in user:
				f.write(',' + decision['prediction'])
			f.write('\n')
		for decision in decisions:
			tmp_statuses = [user['prediction'] for user in decision]
			n_pos = tmp_statuses.count('1') / n_users
			n_neg = tmp_statuses.count('0') / n_users
			n_skip = tmp_statuses.count('2') / n_users
			statistics.append((n_pos, n_neg, n_skip))
		for data in zip(*statistics):
			for point in data:
				f.write(str(point) + ',')
			f.write('\n')


	'''
	So, in the end, the following criteria was used:
	A: Last 3
	B: Last 5
	C: First 3
	D: First 5

	The letters correspond to the filename used to turn in to the contest.
	The following code does not reflect any of that, as it was manually
	modified each time to achieve that.
	'''

	results_file = results_folder + 'CHEPEA_10.txt'
	with open(results_file, 'w') as f:
		for user in last_3:
			prediction = '1' if user['prediction'] == '1' else '2'
			f.write(user['id'] + '\t\t' + prediction + '\n')


	results_file = results_folder + 'CHEPEB_10.txt'
	with open(results_file, 'w') as f:
		for user in last_5:
			prediction = '1' if user['prediction'] == '1' else '2'
			f.write(user['id'] + '\t\t' + prediction + '\n')


	results_file = results_folder + 'CHEPEC_10.txt'
	with open(results_file, 'w') as f:
		for user in first_3:
			prediction = '1' if user['prediction'] == '1' else '2'
			f.write(user['id'] + '\t\t' + prediction + '\n')


	results_file = results_folder + 'CHEPED_10.txt'
	with open(results_file, 'w') as f:
		for user in first_5:
			prediction = '1' if user['prediction'] == '1' else '2'
			f.write(user['id'] + '\t\t' + prediction + '\n')

if __name__ == "__main__":
	main(sys.argv[1:])