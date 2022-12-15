import zutil
import sys
import getopt
import zcsv

### MIF stands for Most Informative Features

def show_most_informative_features(feature_list, clf, n = 200):
	coefs_with_fns = sorted(zip(clf.coef_[0], feature_list))
	n_features = len(feature_list)
	if n_features < n * 2:
		top = zip(coefs_with_fns[:round(n_features / 2)], coefs_with_fns[:-(round(n_features / 2) + 1):-1])
	else:
		top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
	# for (coef_1, fn_1), (coef_2, fn_2) in top:
	# 	print("{:20f}\t{:20}\t{:20f}\t{:20}".format(coef_1, fn_1, coef_2, fn_2))
	return top

# def show_most_informative_features(feature_list, clf):
# 	top = clf.feature_log_prob_
# 	# top = sorted(zip(clf.feature_log_prob_[0], feature_list))
# 	return top

def main(argv):
	# init
	description = 'zmif.py -r <results directory> -t <histogram file> -i <classifier model>'

	# get input argument
	try:
		opts, args = getopt.getopt(argv, "ht:i:r:")
	except getopt.GetoptError:
		print(description)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(description)
			sys.exit()
		elif opt == '-t':
			histogram_file = arg
		elif opt == '-i':
			model_file = arg
		elif opt == '-r':
			results_folder = arg + '/'

	# initialize
	histogram = zutil.loadUser(histogram_file) #lol hax
	classifier = zutil.loadUser(model_file) #lol hax
	mode = 'user' if 'user' in model_file else 'post'
	output_file = results_folder + 'most_informative_features_' + mode + '.csv'

	data = show_most_informative_features(histogram, classifier)
	# print(data)

	formatted_data = [[fn_1, fn_2] for (coef_1, fn_1), (coef_2, fn_2) in data]
	# print(formatted_data)
	zcsv.saveCSV(formatted_data, output_file, ['not depressive', 'depressive'], '\t')

if __name__ == "__main__":
	main(sys.argv[1:])