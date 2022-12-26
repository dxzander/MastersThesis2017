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
	PROC="basic"
else
	CHUNK=$1
	CLF=$2
	PROC=$3
fi

if [ $CLF = "nbc_proba" ]
then
	CLF_MODE="proba"
else
	CLF_MODE="eval"
fi

ROOTF=$HOME/Desktop/$PROC
CNKF=$ROOTF/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA="../Dataset"
RESULTS="../Results"
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
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt

# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

# 13- zxml post
printf 'Loading XML for testing\n'
# normal
python3 zxml.py -m 'user' -g 0 -c $CHUNK -i $TEST -o $TMP
# tfidf
#python3 zxml.py -m 'user' -g 1 -c $CHUNK -i $TEST -o $TMP


# 14- zvec
printf 'Vectorizing\n'
# normal
python3 zvec.py -m 'user' -t "$HIST" -i $TEST
# tfidf
#python3 ztfidf.py -v "$RESULTS" -t "$HIST" -i $TEST

# tmp - save user vectors to csv
#printf "Saving user's vectors to CSV\n"
#python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TEST

# 15- zclf
printf "\nUser-Level Testing - $CLF\n"
python3 zclf.py -m $CLF_MODE -k $CLF -i $TEST -o "$UCLAS"

# 16- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"

# Cleanup
rm -r $CNKF
