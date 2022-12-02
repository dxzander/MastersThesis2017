import zutil
import sys
import getopt
from datetime import datetime, timedelta
import zutc

def discretizer(time):
	# convierte la hora en las regiones establecidas:
	# t- primera transición, 5-7
	# m- mañana, 8-13
	# tt- segunda transición, 14-17
	# n- noche, 18-4
	# w- weekend, whole sat and sun
	if time.weekday() > 4:
		discrete_time = 'w'
	else:
		if time.hour >= 5 and time.hour <= 7:
			discrete_time = 't'
		elif time.hour >= 8 and time.hour <= 13:
			discrete_time = 'm'
		elif time.hour >= 14 and time.hour <= 17:
			discrete_time = 'tt'
		else:
			discrete_time = 'n'
	return discrete_time

def sincronizer(user_texts, user_times):
	# genera representación de usuario en base a tokens con temporalidad
	new_user = []
	for post in zip(user_texts, user_times):
		new_user.append(getToken(post[0], post[1]))
	return new_user

def getToken(post, time):
	# genera el token con temporalidad para cada post
	token = discretizer(time) + str(post)
	# token = discretizer(time)
	return token

def getTimeStats(user_texts, user_times, histogram):
	# saca estadísticas de los tokens de cada usuario
	valid_tokens = ['t0', 'm0', 'tt0', 'n0', 'w0', 't1', 'm1', 'tt1', 'n1', 'w1']
	# valid_tokens = ['t', 'm', 'tt', 'n', 'w']
	new_user = sincronizer(user_texts, user_times)
	user_size = len(new_user)
	# process used in contest...
	#new_user = [round(new_user.count(token) / user_size * 100, 4) for token in histogram]
	# fixed contest
	new_user = [round(new_user.count(token) / user_size * 100, 4) for token in histogram if token in valid_tokens]
	return new_user

# las siguientes librerías son importadas de zutc
# getBaseStats
# getStats

def main(argv):
	# init
	description = 'ztrans.py -m <mode: full|ig|stats> -t <histogram file> -i <input file>'

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
			if arg == 'full' or arg == 'ig' or arg == 'stats':
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
		histogram = ['t0', 'm0', 'tt0', 'n0', 'w0', 't1', 'm1', 'tt1', 'n1', 'w1']
		# histogram = ['t', 'm', 'tt', 'n', 'w']
		zutil.saveUser(['pos', 'neg', 'negpos', 'posneg', 'negneg', 'pospos'] + histogram, histogram_file) #lol hax
	elif mode == 'ig' or mode == 'stats':
		histogram = zutil.loadUser(histogram_file) #lol hax

	# create new user representation
	for file in input_files:
		user = zutil.loadUser(file)
		user_texts = zutil.getUserTexts(user)
		user_times = zutil.getUserTimes(user)
		user_time_stats = getTimeStats(user_texts, user_times, histogram)
		user_stats = zutc.getStats(user_texts)
		if mode == 'stats':
			user_base_stats = zutc.getBaseStats(user_times)
			new_user_texts = [user_stats + user_time_stats + user_base_stats]
		else:
			new_user_texts = [user_stats + user_time_stats]
		new_user = zutil.saveUserNewRepresentation(user, new_user_texts)
		zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])