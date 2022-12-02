#!/bin/bash

# intialize script
#CORES=$(grep -c ^processor /proc/cpuinfo)

if [ $# -eq 0 ]
then
	CHUNK=1
	CLF="nbc"
	PROC="weeksenti"
else
	CHUNK=$1
	CLF=$2
	PROC=$3
fi

ROOTF=$HOME/Desktop/$PROC
CNKF=$ROOTF/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA=$HOME/ownCloud/Maestría/Datasets/reddit-depression
RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
MODE="post_senti_${CLF}_user_weekly_activity"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
TOKH="$RESULTS/tokens_${PROC}_user.pkl"
UCLAS="$RESULTS/model_${PROC}_${CLF}_user.pkl"
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt

# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

# 12- zxml post
printf 'Loading XML for testing\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TEST -o $TMP

# 13- zsenti
printf 'Vectorizing for testing\n'
python3 zsenti.py -m 'full' -i $TEST

# 14- zwsa
printf "\nGetting user's weekly activity for testing\n"
python3 zwsa.py -m 'ig' -t "$TOKH" -i $TEST

# 15- zclf
#printf "\nUser-Level Testing - $CLF\n"
#python3 zclf.py -m 'eval' -k $CLF -i $TEST -o "$UCLAS"

# 16- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"