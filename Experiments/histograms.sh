#!/bin/bash

#  1- zinit        : initialize variables and settings
#   -              : loop to get histogram of all ngrams
#  2- zxml user    : open from xml and combine all texts into one
#  3- zcount       : count terms and create histogram

# intialize script
#CORES=$(grep -c ^processor /proc/cpuinfo)

CHUNK=1
CNKF=$HOME/Desktop/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA=$HOME/ownCloud/Maestría/Datasets/reddit-depression
RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
HIST=$VAR/histogram.pkl
TOKH=$VAR/tokens.pkl
TERMS=-1
NGRAM=0
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt


# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

printf '\nGetting words from '$NGRAM'-grams\n'

# 2- zxml post
printf 'Loading XML for '$NGRAM'-grams\n'
python3 zxml.py -m 'user' -g $NGRAM -c $CHUNK -i $TRAIN -o $TMP

# 3- zcount
printf 'Creating histogram for '$NGRAM'-grams\n'
# n 0 = pareto
# n -1 = any over 1
python3 zcount.py -v $VAR -r "$RESULTS" -g $NGRAM -m 'class' -n $TERMS -i $TRAIN

# Cleanup
rm -r $CNKF