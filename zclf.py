import zutil
import sys
import getopt
import numpy as np
from sklearn.metrics import classification_report

def getClassifier(selection):
	if 'nbc' in selection:
		from sklearn.naive_bayes import MultinomialNB
		classifier = MultinomialNB()
		# classifier = MultinomialNB(class_prior = [1, 1])
	elif selection == 'svm':
		# kernels:
		# linear
		# poly
		# rbf
		# sigmoid
		from sklearn.svm import SVC
		from sklearn.model_selection import GridSearchCV
		tuned_parameters = {
			'C': [i / 10 for i in range(5, 20, 5)],
			'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
			'gamma': ['auto'] + [i / 10 for i in range(0, 11, 2)],
			'coef0': [i / 10 for i in range(0, 11, 2)],
			}
		classifier = GridSearchCV(SVC(), tuned_parameters, n_jobs = 3)

		# classifier = SVC(kernel='linear')

		# from sklearn.svm import LinearSVC
		# from sklearn.model_selection import GridSearchCV
		# tuned_parameters = { #necesita corregirse con parámetros específicos de linear svc
		# 	'C': [i / 10 for i in range(5, 20, 5)],
		# 	'gamma': ['auto'] + [i / 10 for i in range(0, 11, 2)],
		# 	'coef0': [i / 10 for i in range(0, 11, 2)],
		# 	}
		# classifier = GridSearchCV(LinearSVC(), tuned_parameters, n_jobs = 3)
	elif selection == 'knn':
		from sklearn.neighbors import KNeighborsClassifier
		classifier = KNeighborsClassifier(n_neighbors = 5)
	return classifier

def getUserClasses(status, n_texts):
	classes = [status for text in range(n_texts)]
	return classes

def main(argv):
	# init
	description = 'zclf.py -m <mode: train|test|eval|proba|inhe> -v <var directory> -r <results directory> -k <classifier: nbc|svm> -n <partial train max users> -i <input file> -o <model output> -f <filtering? y|n>'
	# use max users = 0 to train on all users instead of partial training
	max_users = 100
	filtering = False

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "hm:v:r:k:n:i:o:f:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-m':
			if arg == 'train' or arg == 'test' or arg == 'eval' or arg == 'proba' or arg == 'inhe':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-v':
			var_folder = arg + '/'
		elif opt == '-r':
			results_folder = arg + '/'
		elif opt == '-k':
			selected_classifier = arg
		elif opt == '-n':
			max_users = int(arg)
		elif opt == '-i':
			list_file = arg
		elif opt == '-o':
			model_file = arg
		elif opt == '-f':
			if arg == 'y':
				filtering = True
		
	# initialize
	input_files = zutil.getUserList(list_file)
	
	if mode == 'train':
		# train mode

		# initialize
		classifier = getClassifier(selected_classifier)
		training_texts = []
		training_classes = []
		total_classes = [0, 1]
		curuser = 0
		
		# load data
		print('Loading Training Texts')
		for file in input_files:
			user = zutil.loadUser(file)
			user_texts = zutil.getUserTexts(user)
			training_texts += user_texts
			training_classes += getUserClasses(user['status'], len(user_texts))
			curuser += 1
			if 'nbc' in selected_classifier:
				if max_users != 0:
					if curuser % max_users == 0:
						print('Partialy Training', end = '\r')
						classifier.partial_fit(training_texts, training_classes, total_classes)
						training_texts = []
						training_classes = []

		# train
		if 'nbc' in selected_classifier:
			if max_users == 0:
				print('Training')
				classifier.fit(training_texts, training_classes)
			else:
				print('Completing Training')
				classifier.partial_fit(training_texts, training_classes, total_classes)
		else:
			print('Training')
			classifier.fit(training_texts, training_classes)
		
		# save
		zutil.saveUser(classifier, model_file) #lol hax
			
	elif mode == 'test':
		# test mode

		# initialize
		testing_classes = []
		classifier = zutil.loadUser(model_file) #lol hax
		predicted_classes = []
		target_names = ['not depressed', 'depressed']
		mode_file = var_folder + 'mode.txt'
		post_mode = zutil.getUserList(mode_file) #lol hax
		
		# load data
		print('Loading Testing Texts')
		for file in input_files:
			user = zutil.loadUser(file)
			testing_texts = zutil.getUserTexts(user)
			testing_classes += getUserClasses(user['status'], len(testing_texts))
			predicted_classes += classifier.predict(testing_texts)

		# test
		print('Classifying')
		report = classification_report(testing_classes, predicted_classes, target_names = target_names, digits = 4)
		print(report)

		# save
		with open(results_folder + post_mode + '_post_results.txt', 'a') as f:
			print(report, file = f)
			print('Saved results to file!\n')

	elif mode == 'inhe':
		# user label inheritance mode

		# initialize

		# load user and create new vector
		for file in input_files:
			user = zutil.loadUser(file)
			user_texts = zutil.getUserTexts(user)
			predicted_texts = [user['status'] for x in range(len(user_texts))]
			new_user = zutil.saveUserTexts(user, predicted_texts)
			zutil.saveUser(new_user, file)

	elif mode == 'eval':
		# user evaluation mode

		# initialize
		classifier = zutil.loadUser(model_file) #lol hax

		# load user and create new vector
		for file in input_files:
			user = zutil.loadUser(file)
			user_texts = zutil.getUserTexts(user)
			predicted_texts = classifier.predict(user_texts)
			new_user = zutil.saveUserTexts(user, predicted_texts)
			if filtering:
				zutil.saveUser(new_user, file.replace('.pkl', '_fil.pkl'))
			else:
				zutil.saveUser(new_user, file)

	elif mode == 'proba':
		# user evaluation mode with probabilities

		# initialize
		classifier = zutil.loadUser(model_file) #lol hax

		# load user and create new vector
		for file in input_files:
			user = zutil.loadUser(file)
			user_texts = zutil.getUserTexts(user)
			predicted_texts = classifier.predict_proba(user_texts)
			# classes = [0, 1]
			# predicted_texts.tolist()
			# predicted_texts = [list(zip(text, classes)) for text in predicted_texts]
			# predicted_texts = [float(text[1][0]) for text in predicted_texts]
			predicted_texts = [text[0] for text in predicted_texts]
			new_user = zutil.saveUserTexts(user, predicted_texts)
			zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])
