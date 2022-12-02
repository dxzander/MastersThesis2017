import zutil
import sys
import getopt
from datetime import datetime, timedelta
import zutc

# discretizer is imported from zutc

def getToken(time):
	# genera el token con temporalidad para cada post
	token = zutc.discretizer(time) + str(time.weekday())
	return token

def sincronizer(user_times):
	# genera representación de usuario en base a tokens con temporalidad
	new_user = []
	for post in user_times:
		new_user.append(getToken(post))
	return new_user

def getTimeVector(user_times, histogram):
	# saca estadísticas de los tokens de cada usuario
	new_user = sincronizer(user_times)
	user_size = len(new_user)
	new_user = [round(new_user.count(token) / user_size, 4) for token in histogram]
	return new_user

def getPeriodVector(user_times, histogram):
	# saca estadísticas de los tokens de cada usuario
	user_texts = [''] * 16 #lol workaround
	new_user = zutc.sincronizer(user_texts, user_times, void='n')
	user_size = len(new_user)
	new_user = [round(new_user.count(token) / user_size, 4) for token in histogram]
	return new_user

def getHourVector(user_times, histogram):
	# saca estadísticas de los tokens de cada usuario
	new_user = []
	for time in user_times:
		new_user.append(str(time.hour))
	user_size = len(new_user)
	new_user = [round(new_user.count(token) / user_size, 4) for token in histogram]
	return new_user

# getBaseStats is imported from zutc

def main(argv):
	# init
	description = 'ztime.py -m <mode: full|stats|hour|period> -i <input file>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:i:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			if arg == 'full' or arg == 'stats' or arg == 'hour' or arg == 'period':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-i':
			list_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)
	if mode == 'hour':
		histogram = [str(hour) for hour in range(0, 24)]
	elif mode == 'full':
		histogram = [period + str(day) for day in range(0, 7) for period in ['m', 't', 'n']]
	elif mode == 'period':
		histogram = ['m', 't', 'n']

	# create new user representation
	for file in input_files:
		user = zutil.loadUser(file)
		user_times = zutil.getUserTimes(user)
		if mode == 'hour':
			user_time_vector = getHourVector(user_times, histogram)
		elif mode == 'full':
			user_time_vector = getTimeVector(user_times, histogram)
		elif mode == 'period':
			user_time_vector = getPeriodVector(user_times, histogram)

		if mode == 'stats':
			user_base_stats = zutc.getBaseStats(user_times)
			new_user_texts = [user_time_vector + user_base_stats]
		else:
			new_user_texts = [user_time_vector]
		new_user = zutil.saveUserNewRepresentation(user, new_user_texts)
		zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])