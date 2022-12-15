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
	CHUNK=1
	CLF="nbc"
else
	CHUNK=$1
	CLF=$2
fi

if [ $CLF = "nbc_proba" ]
then
	CLF_MODE="proba"
else
	CLF_MODE="eval"
fi

CNKF=$HOME/Desktop/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA=$HOME/ownCloud/Maestría/Datasets/reddit-depression
RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
HIST=$VAR/histogram.pkl
TOKH=$VAR/tokens.pkl
WEKA=$VAR/data.arff
IG=$VAR/ig.arff
TERMS=10000
PART=100
MODE="${CLF}_user_bow_ngram_ig"
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt

### TRAINING PHASE

# set title
echo '\033]2;Training for '$CHUNK' chunks\007'

# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

### comment from here to remove ngrams

# begin loop
for NGRAM in 1 2 3
do

	printf '\nGetting words from '$NGRAM'-grams\n'

	# 2- zxml post
	printf 'Loading XML for '$NGRAM'-grams\n'
	python3 zxml.py -m 'user' -g $NGRAM -c $CHUNK -i $TRAIN -o $TMP

	# 3- zcount
	printf 'Creating histogram for '$NGRAM'-grams\n'
	# n 0 = pareto
	# n -1 = any over 1
	python3 zcount.py -v $VAR -g $NGRAM -n $TERMS -i $TRAIN

done
# end loop

# 4- zmerge
printf '\nMerging Histograms\n'
python3 zmerge.py -v $VAR

### end comment for ngram removal

### if no ngram, use this

#printf '\nGetting words\n'

## 2- zxml post
#printf 'Loading XML\n'
#python3 zxml.py -m 'user' -g 1 -c $CHUNK -i $TRAIN -o $TMP

## 3- zcount
#printf 'Creating histogram\n'
## n 0 = pareto
## n -1 = any over 1
#python3 zcount.py -v $VAR -g "" -n $TERMS -i $TRAIN

### end of code for no ngram

# 5- zxml user
printf '\nLoading XML for IG\n'
python3 zxml.py -m 'user' -g 0 -c $CHUNK -i $TRAIN -o $TMP

# 6- zvec
printf 'Vectorizing for IG\n'
python3 zvec.py -m 'user' -t $HIST -i $TRAIN

# 7- zweka export
printf '\nExporting to weka\n'
python3 zweka.py -m 'export' -t $HIST -w $WEKA -i $TRAIN -o $TMP

# 8- weka
printf 'Calculating Information Gain...\n'
java -Xmx5000m -classpath "$HOME/Downloads/weka/weka.jar" \
weka.filters.supervised.attribute.AttributeSelection \
-E "weka.attributeSelection.InfoGainAttributeEval" \
-S "weka.attributeSelection.Ranker -T 0 -N -1" \
-i $WEKA -o $IG

# 9- zweka import
printf 'Importing from weka\n'
python3 zweka.py -m 'import' -c $CHUNK -r "$RESULTS" -t $HIST -w $IG -o $TMP

# 10- zxml post
printf '\nReloading XML for training\n'
python3 zxml.py -m 'user' -g 0 -c $CHUNK -i $TRAIN -o $TMP

# 11- zvec
printf 'Vectorizing for training\n'
python3 zvec.py -m 'user' -t $HIST -i $TRAIN

# tmp - save user vectors to csv
#printf "Saving user's vectors to CSV\n"
#python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TRAIN

# 12- zclf train
printf "\nUser-Level Training - $CLF\n"
python3 zclf.py -m 'train' -k $CLF -i $TRAIN -o "$RESULTS/model_${CHUNK}_${CLF}_user.pkl"

### TESTING PHASE

# set title
echo '\033]2;Evaluating on '$CHUNK' chunks\007'

# 13- zxml post
printf 'Loading XML for testing\n'
python3 zxml.py -m 'user' -g 0 -c $CHUNK -i $TEST -o $TMP

# 14- zvec
printf 'Vectorizing\n'
python3 zvec.py -m 'user' -t $HIST -i $TEST

# tmp - save user vectors to csv
#printf "Saving user's vectors to CSV\n"
#python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TEST

# 15- zclf
printf "\nUser-Level Testing - $CLF\n"
python3 zclf.py -m $CLF_MODE -k $CLF -i $TEST -o "$RESULTS/model_${CHUNK}_${CLF}_user.pkl"

# 16- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"

# Cleanup
rm -r $CNKF