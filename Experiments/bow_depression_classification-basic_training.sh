#!/bin/bash

#   -              : training begins
#  1- zinit        : initialize variables and settings
#   -              : loop to get histogram of all ngrams
#  2- zxml user    : open from xml and combine all texts into one
#  3- zcount       : count terms and create histogram
#   -              : end loop
#  4- zmerge       : combine all histograms
#  5- zxml user    : open from xml and combine all texts into one
#  6- zvec         : convert texts to vectors from histogram
#  7- zweka export : exports words data to weka
#  8- weka         : weka lol (ranks attributes by IG and selects all non zero)
#  9- zweka import : imports words data from weka
# 10- zxml user    : open from xml and combine all texts into one
# 11- zvec         : convert texts to vectors from histogram
# 12- zclf train   : train NBC from vectors. post lvl
#   -              : testing begins
# 24- zxml user    : open from xml and combine all texts into one
# 25- zvec         : convert texts to vectors from histogram
# 29- zres         : classify users and save results to file

# intialize script
#CORES=$(grep -c ^processor /proc/cpuinfo)

if [ $# -eq 0 ]
then
	CLF="nbc"
	PROC="contest"
else
	CLF=$1
	PROC=$2
fi

CHUNK=1
ROOTF=$HOME/Desktop/$PROC
CNKF=$ROOTF/train
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA=$HOME/ownCloud/Maestría/Datasets/reddit-depression
RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
MODE="${CLF}_user_bow_ngram_ig"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
if [ $CLF = "nbc_proba" ]
then
	PCLAS="$RESULTS/model_${PROC}_nbc_post.pkl"
	UCLAS="$RESULTS/model_${PROC}_nbc_user.pkl"
else
	PCLAS="$RESULTS/model_${PROC}_${CLF}_post.pkl"
	UCLAS="$RESULTS/model_${PROC}_${CLF}_user.pkl"
fi
HIST="$RESULTS/histogram_${PROC}_post.pkl"
TOKH="$RESULTS/tokens_${PROC}_user.pkl"
WEKA=$VAR/data.arff
IG=$VAR/ig.arff
TERMS=10000
PART=0
mkdir $ROOTF
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt

### TRAINING PHASE

# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

### comment from here to remove ngrams

# begin loop
#for NGRAM in 1 2 3
#do

#	printf '\nGetting words from '$NGRAM'-grams\n'

#	# 2- zxml post
#	printf 'Loading XML for '$NGRAM'-grams\n'
#	python3 zxml.py -m 'user' -g $NGRAM -i $TRAIN -o $TMP

#	# 3- zcount
#	printf 'Creating histogram for '$NGRAM'-grams\n'
#	# n 0 = pareto
#	# n -1 = any over 1
#	python3 zcount.py -v $VAR -g $NGRAM -n $TERMS -i $TRAIN

#done
## end loop

## 4- zmerge
#printf '\nMerging Histograms\n'
#python3 zmerge.py -v $VAR -t "$HIST"

### end comment for ngram removal

### if no ngram, use this

printf '\nGetting words\n'

# 2- zxml post
printf 'Loading XML\n'
python3 zxml.py -m 'user' -g 1 -i $TRAIN -o $TMP

# 3- zcount
printf 'Creating histogram\n'
# n 0 = pareto
# n -1 = any over 1
python3 zcount.py -v $VAR -g "" -n $TERMS -i $TRAIN

### end of code for no ngram

# 5- zxml user
printf '\nLoading XML for IG\n'
python3 zxml.py -m 'user' -g 0 -i $TRAIN -o $TMP

# 6- zvec
printf 'Vectorizing for IG\n'
python3 zvec.py -m 'user' -t "$HIST" -i $TRAIN


# 7- zweka export
printf '\nExporting to weka\n'
python3 zweka.py -m 'export' -t "$HIST" -w $WEKA -i $TRAIN -o $TMP

# 8- weka
printf 'Calculating Information Gain...\n'
java -Xmx5000m -classpath "$HOME/Downloads/weka/weka.jar" \
weka.filters.supervised.attribute.AttributeSelection \
-E "weka.attributeSelection.InfoGainAttributeEval" \
-S "weka.attributeSelection.Ranker -T 0 -N -1" \
-i $WEKA -o $IG

# 9- zweka import
printf 'Importing from weka\n'
python3 zweka.py -m 'import' -c $CHUNK -r "$RESULTS" -t "$HIST" -w $IG -o $TMP

# 10- zxml post
printf '\nReloading XML for training\n'
# normal
python3 zxml.py -m 'user' -g 0 -i $TRAIN -o $TMP
# for tfidf
#python3 zxml.py -m 'user' -g 1 -i $TRAIN -o $TMP

# 11- zvec
printf 'Vectorizing for training\n'
# normal
python3 zvec.py -m 'user' -t "$HIST" -i $TRAIN
# tfidf
#python3 ztfidf.py -v "$RESULTS" -t "$HIST" -i $TRAIN

# tmp - save user vectors to csv
#printf "Saving user's vectors to CSV\n"
#python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TRAIN

# 12- zclf train
printf "\nUser-Level Training - $CLF\n"
python3 zclf.py -m 'train' -k $CLF -n $PART -i $TRAIN -o "$UCLAS"