#!/bin/bash

RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
EVAL="$HOME/ownCloud/Maestría/Datasets/reddit-depression/training/scripts evaluation"
CLF="svm"
PROC="contest"
ROOTF=$HOME/Desktop/$PROC
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_time"
TOTAL=10
mkdir $ROOTF

# set title
echo '\033]2;Training\007'

sh two-step_depression_classification-contest_training.sh $CLF $PROC

# set title
echo '\033]2;Testing\007'

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-contest_testing.sh $x $CLF $PROC &
done

echo "Waiting for $TOTAL jobs to finish"
wait

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p "n"

# ERDE calculation
./erde_test.sh

# Cleanup
rm -r $ROOTF