import zutil
import sys
import getopt
from datetime import datetime, timedelta
import numpy as np

### WAM stands for Week Activity Module

def createEmptyWeekActivity():
	hours = [i for i in range(0, 24)]
	days = [i for i in range(0, 7)]
	new_user = [[0 for hour in hours] for day in days]
	return new_user

def createWeekActivity(user_times):
	new_user = createEmptyWeekActivity()
	for time in user_times:
		day = time.weekday()
		hour = time.hour
		new_user[day][hour] += 1
	return new_user

# original
def normalizeWeekActivity(week_activity):
	total_activity = sum(sum(week_activity, []))
	new_user = [[hour / total_activity for hour in day] for day in week_activity]
	return new_user

# tests
# def normalizeWeekActivity(week_activity):
# 	total_activity = sum(sum(week_activity, []))
# 	new_user = [[round(hour / total_activity * 1000, 1) for hour in day] for day in week_activity]
# 	return new_user

# def normalizeWeekActivity(week_activity):
	# return week_activity

def sumWeekActivities(week_activity_1, week_activity_2):
	hours = [hour for hour in range(len(week_activity_1[0]))]
	days = [day for day in range(len(week_activity_1))]
	new_user = [[week_activity_1[day][hour] + week_activity_2[day][hour] for hour in hours] for day in days]
	return new_user

def getUserClass(week_activity, neg_prototype, pos_prototype):
	neg_coef = np.corrcoef(week_activity, neg_prototype)[1, 0]
	pos_coef = np.corrcoef(week_activity, pos_prototype)[1, 0]
	decision = 0 if neg_coef > pos_coef else 1
	return decision

def main(argv):
	# init
	description = 'zwam.py -m <mode: proto|vec|comp> -t <prototypes file> -i <input file>'

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
			if arg == 'proto' or arg == 'vec' or arg == 'comp':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-t':
			prototypes_file = arg
		elif opt == '-i':
			list_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)
	if mode == 'comp':
		prototypes = zutil.loadUser(prototypes_file) #lol hax
	elif mode == 'proto':
		prototypes = [createEmptyWeekActivity(), createEmptyWeekActivity()]

	#start
	for file in input_files:
		user = zutil.loadUser(file)
		# cargar o crear actividad de usuario
		if mode == 'proto' or mode == 'vec':
			user_times = zutil.getUserTimes(user)
			user_week_activity = createWeekActivity(user_times)
		elif mode == 'comp':
			user_week_activity = zutil.getUserTexts(user)[0]

		# trabajar con la actividad de usuario
		if mode == 'proto':
			status = user['status']
			prototypes[status] = sumWeekActivities(user_week_activity, prototypes[status])
		elif mode == 'vec':
			user_week_activity = normalizeWeekActivity(user_week_activity)
			new_user = zutil.saveUserNewRepresentation(user, [user_week_activity])
		elif mode == 'comp':
			predicted_class = getUserClass(user_week_activity, prototypes[0], prototypes[1])
			new_user = zutil.saveUserTexts(user, [predicted_class])

		# guardar actividad de usuario
		if mode == 'vec' or mode == 'comp':
			zutil.saveUser(new_user, file)

	# for prototyping only
	if mode == 'proto':
		prototypes = [normalizeWeekActivity(prototype) for prototype in prototypes]
		# for prototype in prototypes:
		# 	print('\nPrototype')
		# 	for day in prototype:
		# 		print(day)
		zutil.saveUser(prototypes, prototypes_file) #lol hax

if __name__ == "__main__":
	main(sys.argv[1:])