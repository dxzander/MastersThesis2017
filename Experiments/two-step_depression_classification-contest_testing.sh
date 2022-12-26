#!/bin/bash

#  1- zinit        : initialize variables and settings
# 24- zxml post    : open from xml and leave all posts intact
# 25- zvec         : convert texts to vectors from histogram
# 26- zclf eval    : classify each user's post to create a vector representation
# 27- zutc         : create a new user representation through statistics
# 28- zclf eval    : classify each user
# 29- zres         : classify users and save results to file

# Originalmente se prevía que sería de 20 pasos

# intialize script
#CORES=$(grep -c ^processor /proc/cpuinfo)

if [ $# -eq 0 ]
then
	CHUNK=1
	CLF="nbc"
	PROC="contest"
else
	CHUNK=$1
	CLF=$2
	PROC=$3
fi

if [ $CLF = "nbc" ]
then
	CLF_MODE="eval"
else
	CLF_MODE="proba"
fi

ROOTF=$HOME/Desktop/$PROC
CNKF=$ROOTF/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA="../Dataset"
RESULTS="../Results"
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_time"
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

# 23- zxml post
printf 'Loading XML for testing\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TEST -o $TMP

# 24- zvec
printf 'Vectorizing\n'
python3 zvec.py -m 'post' -t "$HIST" -i $TEST

# 25- zclf eval
printf '\nClassifying User Texts\n'
python3 zclf.py -m 'eval' -k $CLF -i $TEST -o "$PCLAS"

# 26- zutc
printf "Getting user's statistics\n"
python3 zutc.py -m 'ig' -t "$TOKH" -i $TEST

# tmp - save user vectors to csv
#printf "Saving user's vectors to CSV\n"
#python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TEST

# 27- zclf
printf "\nUser-Level Testing - $CLF\n"
python3 zclf.py -m $CLF_MODE -k $CLF -i $TEST -o "$UCLAS"

# 28- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"