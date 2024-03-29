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
# 10- zxml post    : open from xml and leave all posts intact
# 11- zvec         : convert texts to vectors from histogram
# 12- zclf train   : train NBC from vectors. post lvl
# 13- zclf eval    : classify each user's post to create a vector representation
# 14- zutc         : create a new user representation through statistics using all tokens
# 15- zweka export : exports token data to weka
# 16- weka         : weka lol (ranks attributes by IG and selects all non zero)
# 17- zweka import : imports token data from weka
# 18- zxml post    : open from xml and leave all posts intact
# 19- zvec         : convert texts to vectors from histogram
# 20- zclf train   : train NBC from vectors. post lvl
# 21- zclf eval    : classify each user's post to create a vector representation
# 22- zutc         : create a new user representation through statistics using ig tokens
# 23- zclf train   : train NBC from vectors. user lvl
#   -              : testing begins
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
else
	CHUNK=$1
	CLF=$2
fi

CNKF=$HOME/Desktop/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA="../Dataset"
RESULTS="../Results"
MODE="post_senti_${CLF}_user_stats_time"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
HIST=$VAR/histogram.pkl
TOKH=$VAR/tokens.pkl
WEKA=$VAR/data.arff
IG=$VAR/ig.arff
TERMS=10000
PART=50
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
printf 'Loading XML for 1-grams\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TRAIN -o $TMP

# 3 - zsenti
printf 'Vectorizing for training\n'
python3 zsenti.py -m 'disc' -i $TRAIN

# 4- zutc
printf "\nGetting user's statistics for training\n"
python3 zutc.py -m 'novoid' -t $TOKH -i $TRAIN

# 5- zclf train
printf "\nUser-Level Training - $CLF\n"
python3 zclf.py -m 'train' -k $CLF -i $TRAIN -o "$RESULTS/model_${CHUNK}_${CLF}_user.pkl"

### TESTING PHASE

# set title
echo '\033]2;Evaluating on '$CHUNK' chunks\007'

#use new mode without join negation
# 6- zxml post
printf 'Loading XML for testing\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TEST -o $TMP

# 7- zsenti
printf 'Vectorizing for testing\n'
python3 zsenti.py -m 'disc' -i $TEST

# 8- zutc
printf "Getting user's statistics\n"
python3 zutc.py -m 'ig' -t $TOKH -i $TEST

# 9- zclf
printf "\nUser-Level Testing - $CLF\n"
python3 zclf.py -m 'eval' -k $CLF -i $TEST -o "$RESULTS/model_${CHUNK}_${CLF}_user.pkl"

# 10- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"

# Cleanup
rm -r $CNKF