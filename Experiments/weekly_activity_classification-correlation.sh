#!/bin/bash

#   -              : training begins
#  1- zinit        : initialize variables and settings
#  2- zxml post    : open from xml and combine all texts into one
#  3- zwam proto   : create week activity prototypes for both classes
#   -              : testing begins
#  4- zxml post    : open from xml and leave all posts intact
#  5- zwam vec     : create week activity vectors for each user
#  6- zwam comp    : decide class for each user by comparing to prototipes
#  7- zres         : classify users and save results to file


# intialize script
#CORES=$(grep -c ^processor /proc/cpuinfo)

if [ $# -eq 0 ]
then
	CHUNK=1
else
	CHUNK=$1
fi

CNKF=$HOME/Desktop/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA="../Dataset"
RESULTS="../Results"
MODE="user_week_activity"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
PROT=$VAR/prototypes.pkl
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

# 3- zwam proto
printf '\nCreating week activity prototypes\n'
python3 zwam.py -m 'proto' -t $PROT -i $TRAIN

### TESTING PHASE

# set title
echo '\033]2;Evaluating on '$CHUNK' chunks\007'

# 4- zxml post
printf 'Loading XML for testing\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TEST -o $TMP

# 5- zwam vec
printf '\nCreating week activity for each user\n'
python3 zwam.py -m 'vec' -i $TEST

# 6- zwam compare
printf '\ncomparing week activity and classifying\n'
python3 zwam.py -m 'comp' -t $PROT -i $TEST

# 7- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"

# Cleanup
rm -r $CNKF