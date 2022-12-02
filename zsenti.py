import zutil
import sys
import getopt
sys.path.insert(0, '/home/zander/ownCloud/Maestría/Proyectos/Senticnet') # needed for senticnet
import senticnet

def valueRemapper(OldValue, OldMax, OldMin, NewMax, NewMin):
	# OldRange = (OldMax - OldMin)
	# NewRange = (NewMax - NewMin)
	# NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	NewValue = (((OldValue - OldMin) * (NewMax - NewMin)) / (OldMax - OldMin)) + NewMin
	return NewValue

def sentimentAnalyzer(text):
	scnet = senticnet.Senticnet()
	concepts = scnet.data.keys()
	polarity = 0
	n_concepts = 0

	for word in text:
		if word in concepts:
			concept_data = scnet.concept(word)
			polarity += -1 if concept_data['polarity'] == 'negative' else 1
			n_concepts += 1

	if n_concepts != 0:
		polarity = round(polarity / n_concepts, 4)
		polarity = valueRemapper(polarity, 1, -1, 1, 0)

	return polarity

def sentimentAnalyzerFull(text):
	### Vector values
	# polarity
	# attention
	# pleasantness
	# aptitude
	# sensitivity

	scnet = senticnet.Senticnet()
	concepts = scnet.data.keys()
	scores = [0, 0, 0, 0, 0]
	n_concepts = 0

	for word in text:
		if word in concepts:
			concept_data = scnet.concept(word)
			scores[0] += -1 if concept_data['polarity'] == 'negative' else 1
			scores[1] += float(concept_data['sentics']['attention'])
			scores[2] += float(concept_data['sentics']['pleasantness'])
			scores[3] += float(concept_data['sentics']['aptitude'])
			scores[4] += float(concept_data['sentics']['sensitivity'])
			n_concepts += 1

	if n_concepts != 0:
		scores = [round(score / n_concepts, 4) for score in scores]
		scores = [valueRemapper(score, 1, -1, 1, 0) for score in scores]

	return scores

def sentiDiscretizer(sentiment):
	if sentiment > 0.5:
		discretized_sentiment = 0
	else:
		discretized_sentiment = 1
	return discretized_sentiment

def main(argv):
	# init
	description = 'zsenti.py -m <mode: full|disc|senti> -i <list of input files>'

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
			if arg == 'full' or arg == 'disc' or arg == 'senti':
				mode = arg
			else:
				print('Error: invalid mode or not specified.')
				sys.exit(2)
		elif opt == '-i':
			list_file = arg

	# initialize
	input_files = zutil.getUserList(list_file)

	# process text
	for file in input_files:
		user = zutil.loadUser(file)
		user_texts = zutil.getUserTexts(user)
		if mode == 'full':
			sentiments = [sentimentAnalyzerFull(user_text) for user_text in user_texts]
		elif mode == 'disc':
			sentiments = [sentiDiscretizer(sentimentAnalyzer(user_text)) for user_text in user_texts]
		new_user = zutil.saveUserTexts(user, sentiments)
		zutil.saveUser(new_user, file)

if __name__ == "__main__":
	main(sys.argv[1:])