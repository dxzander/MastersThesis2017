#!/bin/bash

#   -              : training begins
#  1- zinit        : initialize variables and settings
#  2- zxml post    : open from xml and leave all posts intact
#  3- ztime        : create a new user representation through time tokens
#  4- zclf train   : train NBC from vectors. user lvl
#   -              : testing begins
#  5- zxml post    : open from xml and leave all posts intact
#  6- ztime        : create a new user representation through time tokens
#  7- zclf eval    : classify each user
#  8- zres         : classify users and save results to file

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
CNKF=$HOME/Desktop/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA=$HOME/ownCloud/Maestría/Datasets/reddit-depression
RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
MODE="${CLF}_user_time"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
PART=0
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

# 2- zxml post
printf '\nLoading XML for training\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TRAIN -o $TMP

# 3- ztime
printf 'Vectorizing for training\n'
python3 ztime.py -m 'full' -i $TRAIN

# tmp - save user vectors to csv
printf "Saving user's vectors to CSV\n"
python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TRAIN

# 4- zclf train
printf "\nUser-Level Training - $CLF\n"
python3 zclf.py -m 'train' -k $CLF -i $TRAIN -o "$RESULTS/model_${CHUNK}_${CLF}_user.pkl"

### TESTING PHASE

# set title
echo '\033]2;Evaluating on '$CHUNK' chunks\007'

# 5- zxml post
printf 'Loading XML for testing\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TEST -o $TMP

# 6- zvec
printf 'Vectorizing\n'
python3 ztime.py -m 'full' -i $TEST

# tmp - save user vectors to csv
printf "Saving user's vectors to CSV\n"
python3 zcsv.py -c $CHUNK -r "$RESULTS" -i $TEST

# 7- zclf
printf "\nUser-Level Testing - $CLF\n"
python3 zclf.py -m 'eval' -k $CLF -i $TEST -o "$RESULTS/model_${CHUNK}_${CLF}_user.pkl"

# 8- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"

# Cleanup
rm -r $CNKF