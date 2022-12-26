#!/bin/bash

if [ $# -eq 0 ]
then
	CHUNK=1
	CLF="nbc"
	PROC="combo"
	TPROC="time"
	WPROC="weekly"
else
	CHUNK=$1
	CLF=$2
	PROC=$3
	TPROC=$4
	WPROC=$5
fi

ROOTF=$HOME/Desktop/$PROC
CNKF=$ROOTF/$CHUNK
TMP=$CNKF/tmp
VAR=$CNKF/var
DATA="../Dataset"
RESULTS="../Results"
MODE="user_stats_time_weekly_activity_${CLF}"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
CLAS="$RESULTS/model_${PROC}_${CLF}_post.pkl"
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt

# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

# 2- zcombo
printf 'Combining vectors\n'
python3 zcombo.py -0 $HOME/Desktop/$PROC -1 $HOME/Desktop/$TPROC -2 $HOME/Desktop/$WPROC -c $CHUNK

# 3- zclf
printf "\nCombined Testing - $CLF\n"
python3 zclf.py -m 'eval' -k $CLF -i $TEST -o "$CLAS"

# 4- zres
printf "Getting classification results\n"
python3 zres.py -i $TEST -o "$RESULTS/${MODE}_$CHUNK.txt"