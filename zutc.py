import zutil
import sys
import getopt
from datetime import datetime, timedelta

def discretizer(time):
	# convierte la hora en mañana, tarde o noche
	# m- mañana, 6-13
	# t- tarde, 14-22
	# n- noche, 22-5
	if time.hour >= 6 and time.hour < 14:
		discrete_time = 'm'
	elif time.hour >= 14 and time.hour < 22:
		discrete_time = 't'
	else:
		discrete_time = 'n'
	return discrete_time

def getToken(post, time):
	# genera el token con temporalidad para cada post
	token = discretizer(time) + str(post)
	return token

def sincronizer(user_texts, user_times, void):
	# genera representación de usuario en base a tokens con temporalidad
	new_user = []
	old_post = False
	for post in zip(user_texts, user_times):
		if void == 'y':
			if old_post:
				fillers = fillVoid(old_post[1], post[1])
				new_user.extend(fillers)
		new_user.append(getToken(post[0], post[1]))
		old_post = post
	return new_user

def fillVoid(old, current):
	# llena huecos de periodos sin publicaciones
	null_token = 'x'
	unit = timedelta(hours = 8)
	fillers = []
	filler = old + unit
	while filler < current:
		if discretizer(filler) != discretizer(current):
			fillers.append(getToken(null_token, filler))
		filler += unit
	return fillers

def getTimeStats(user_texts, user_times, histogram, void):
	# saca estadísticas de los tokens de cada usuario
	valid_tokens = ['m0', 't0', 'n0', 'm1', 't1', 'n1', 'mx', 'tx', 'nx']
	new_user = sincronizer(user_texts, user_times, void)
	user_size = len(new_user)
	# process used in contest...
	#new_user = [round(new_user.count(token) / user_size * 100, 4) for token in histogram]
	# fixed contest
	new_user = [round(new_user.count(token) / user_size * 100, 4) for token in histogram if token in valid_tokens]
	return new_user

def getBaseStats(user_times):
	# counts number of posts and time span of posts
	n_posts = len(user_times)
	time_span = abs(user_times[0] - user_times[-1])
	time_span = time_span / timedelta(days = 1)
	new_user = [n_posts, time_span]
	return new_user

def getStats(user_texts):
	user_size = len(user_texts)
	ratio = [round(len([i for i in user_texts if i == 1]) / user_size * 100, 4), round(len([i for i in user_texts if i == 0]) / user_size * 100, 4)]
	bigrams = [[user_texts[post], user_texts[post + 1]] for post in range(user_size - 1)]
	n_bigrams = len(bigrams)
	if n_bigrams == 0:
		negneg = 0
		pospos = 0
		negpos = 0
		posneg = 0
	else:
		negneg = round(bigrams.count([0, 0]) / n_bigrams * 100, 4)
		pospos = round(bigrams.count([1, 1]) / n_bigrams * 100, 4)
		negpos = round(bigrams.count([0, 1]) / n_bigrams * 100, 4)
		posneg = round(bigrams.count([1, 0]) / n_bigrams * 100, 4)
	new_user = ratio + [negpos, posneg, negneg, pospos]
	return new_user

def main(argv):
	# init
	description = 'zutc.py -m <mode: full|ig|stats|novoid> -t <histogram file> -i <input file>'

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
			if arg == 'full' or arg == 'ig' or arg == 'stats' or arg == 'novoid':
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
	if mode == 'full':
		histogram = ['m0', 't0', 'n0', 'm1', 't1', 'n1', 'mx', 'tx', 'nx']
		zutil.saveUser(['pos', 'neg', 'negpos', 'posneg', 'negneg', 'pospos'] + histogram, histogram_file) #lol hax
	elif mode == 'ig' or mode == 'stats':
		histogram = zutil.loadUser(histogram_file) #lol hax
	elif mode == 'novoid':
		histogram = ['m0', 't0', 'n0', 'm1', 't1', 'n1']
		zutil.saveUser(['pos', 'neg', 'negpos', 'posneg', 'negneg', 'pospos'] + histogram, histogram_file) #lol hax

	# create new user representation
	for file in input_files:
		user = zutil.loadUser(file)
		user_texts = zutil.getUserTexts(user)
		user_times = zutil.getUserTimes(user)
		void = 'n' if mode == 'novoid' else 'y'
		user_time_stats = getTimeStats(user_texts, user_times, histogram, void)
		user_stats = getStats(user_texts)
		if mode == 'stats':
			user_base_stats = getBaseStats(user_times)
			new_user_texts = [user_stats + user_time_stats + user_base_stats]
		else:
			new_user_texts = [user_stats + user_time_stats]
		new_user = zutil.saveUserNewRepresentation(user, new_user_texts)
		zutil.saveUser(new_user, file)

	# original code
	# sync_users = sincronizer(training_users, training_times)
	# sync_users = getTimeStats(sync_users)
	# training_stats = zrc.getStats(training_users)
	# training_users = [user[0] + user[1] for user in zip(training_stats, sync_users)]

if __name__ == "__main__":
	main(sys.argv[1:])