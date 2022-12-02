import zutil
import sys
import getopt
from datetime import datetime, timedelta
import zutc

### WSA stands for Week Sentiment Analysis

def labelsGenerator():
	hours = ['z', 'm', 't', 'n']
	days = ['z', 'l', 'm', 'x', 'j', 'v', 's', 'd', 'w', 'q']
	sentis = ['pol', 'att', 'ple', 'apt', 'sen']
	labels = [(day + hour + '_' + senti, (days.index(day), hours.index(hour), sentis.index(senti))) for day in days for hour in hours for senti in sentis]
	return labels

def createEmptyCounts():
	hours = [i for i in range(0, 4)]
	days = [i for i in range(0, 10)]
	new_user = [[0 for hour in hours] for day in days]
	return new_user

def createEmptyWeekActivity():
	hours = [i for i in range(0, 4)]
	days = [i for i in range(0, 10)]
	new_user = [[[0, 0, 0, 0, 0] for hour in hours] for day in days]
	return new_user

#for counts matrix
def normalizeWeekActivity(week_activity, counts):
	hours = [i for i in range(len(week_activity[0]))]
	days = [i for i in range(len(week_activity))]
	new_user = [[[senti / counts[day][hour] if counts[day][hour] != 0 else 0 for senti in week_activity[day][hour]] for hour in hours] for day in days]
	return new_user

#for num of posts
# def normalizeWeekActivity(week_activity, total):
# 	hours = [i for i in range(0, 4)]
# 	days = [i for i in range(0, 10)]
# 	new_user = [[[senti / total for senti in week_activity[day][hour]] for hour in hours] for day in days]
# 	return new_user

def matrixToVector(user_matrix, histogram):
	full_labels = labelsGenerator()
	# print(full_labels)
	labels = [a for a, b in full_labels]
	# print(labels)
	histogram_positions = [full_labels[labels.index(i)][1] for i in histogram]
	new_user = [user_matrix[day][hour][senti] for day, hour, senti in histogram_positions]
	return new_user

def getWeekActivity(user_texts, user_times, histogram):
	activity = createEmptyWeekActivity()
	counts = createEmptyCounts()
	num_texts = len(user_texts)
	discrete_to_number = {
		'm': 1,
		't': 2,
		'n': 3
	}
	weekdays = [i for i in range(1, 6)]
	weekend = [i for i in range(6, 8)]

	for post in zip(user_texts, user_times):
		day = post[1].weekday() + 1
		hour = zutc.discretizer(post[1])
		# add post
		activity[day][discrete_to_number[hour]] = zutil.sumVectors(activity[day][discrete_to_number[hour]], post[0]) #add to slot
		activity[0][discrete_to_number[hour]] = zutil.sumVectors(activity[0][discrete_to_number[hour]], post[0]) #add to period
		activity[day][0] = zutil.sumVectors(activity[day][0], post[0]) #add to day
		activity[0][0] = zutil.sumVectors(activity[day][0], post[0]) #add to user
		if day in weekdays:
			activity[8][0] = zutil.sumVectors(activity[8][0], post[0])
		elif day in weekend:
			activity[9][0] = zutil.sumVectors(activity[9][0], post[0])
		# count added post
		counts[day][discrete_to_number[hour]] = 1 #count slot
		counts[0][discrete_to_number[hour]] += 1 #count period
		counts[day][0] += 1 #count day
		counts[0][0] += 1 #count user
		if day in weekdays:
			counts[8][0] += 1
		elif day in weekend:
			counts[9][0] += 1

	# average posts
	normalized_activity = normalizeWeekActivity(activity, counts) #for count matrix
	# normalized_activity = normalizeWeekActivity(activity, num_texts) #for num of posts

	# convert matrix to vector
	new_user = matrixToVector(normalized_activity, histogram)
	# new_user = matrixToVector(activity, histogram)
	return new_user

def main(argv):
	# init
	description = 'zwsa.py -m <mode: full|ig|true> -t <histogram file> -i <input file>'

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
			if arg == 'full' or arg == 'ig' or arg == 'true':
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
		labels = labelsGenerator()
		histogram = [a for a, b in labels]
		zutil.saveUser(histogram, histogram_file) #lol hax
	elif mode == 'true':
		labels = labelsGenerator()
		histogram = [a for a, b in labels if 'z' in a]
		zutil.saveUser(histogram, histogram_file) #lol hax
	elif mode == 'ig' or mode == 'stats':
		histogram = zutil.loadUser(histogram_file) #lol hax
	
	# create new user representation
	for file in input_files:
		user = zutil.loadUser(file)
		user_texts = zutil.getUserTexts(user)
		user_times = zutil.getUserTimes(user)
		week_activity = getWeekActivity(user_texts, user_times, histogram)
		new_user_texts = [week_activity]
		new_user = zutil.saveUserNewRepresentation(user, new_user_texts)
		zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])