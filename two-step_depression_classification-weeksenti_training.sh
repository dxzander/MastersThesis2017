#!/bin/bash

# intialize script
#CORES=$(grep -c ^processor /proc/cpuinfo)

if [ $# -eq 0 ]
then
	CLF="nbc"
	PROC="weeksenti"
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
MODE="post_senti_${CLF}_user_weekly_activity"
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
TOKH="$RESULTS/tokens_${PROC}_user.pkl"
WEKA=$VAR/data.arff
IG=$VAR/ig.arff
UCLAS="$RESULTS/model_${PROC}_${CLF}_user.pkl"
TERMS=10000
PART=100
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt

# 1- zinit
printf 'Initializing\n'
python3 zinit.py -v $VAR -c $CHUNK -i $TRAIN -o $TEST

# 2- zxml post
printf 'Loading XML for training\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TRAIN -o $TMP

# 3 - zsenti
printf 'Vectorizing for training\n'
python3 zsenti.py -m 'full' -i $TRAIN

# 4- zwsa
printf "\nGetting user's weekly activity for IG\n"
python3 zwsa.py -m 'full' -t "$TOKH" -i $TRAIN

# 5- zweka export
printf '\nExporting to weka\n'
python3 zweka.py -m 'export' -t "$TOKH" -w $WEKA -i $TRAIN -o $TMP

# 6- weka
printf 'Calculating Information Gain...\n'
java -Xmx5000m -classpath "$HOME/Downloads/weka/weka.jar" \
weka.filters.supervised.attribute.AttributeSelection \
-E "weka.attributeSelection.InfoGainAttributeEval" \
-S "weka.attributeSelection.Ranker -T 0 -N -1" \
-i $WEKA -o $IG

# 7- zweka import
printf 'Importing from weka\n'
python3 zweka.py -m 'import' -c $CHUNK -r "$RESULTS" -t "$TOKH" -w $IG -o $TMP

# 8- zxml post
printf '\nReloading XML for training\n'
python3 zxml.py -m 'post' -g 0 -c $CHUNK -i $TRAIN -o $TMP

# 9- zsenti
printf 'Vectorizing for training\n'
python3 zsenti.py -m 'full' -i $TRAIN

# 10- zwsa
printf "\nGetting user's weekly activity for training\n"
python3 zwsa.py -m 'ig' -t "$TOKH" -i $TRAIN

# 11- zclf train
printf "\nUser-Level Training - $CLF\n"
python3 zclf.py -m 'train' -k $CLF -n $PART -i $TRAIN -o "$UCLAS"

# tmp - save most relevant features to file
printf "\nUser-Level Relevant Features Extraction - $CLF\n"
python3 zmif.py -r "$RESULTS" -t "$TOKH" -i "$UCLAS"