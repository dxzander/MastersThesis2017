#!/bin/bash

RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
EVAL="$HOME/ownCloud/Maestría/Datasets/reddit-depression/training/scripts evaluation"
CLF="nbc"
PROC="contest"
TOTAL=10
ROOTF=$HOME/Desktop/$PROC
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_time"
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

echo "Waiting for 10 jobs to finish"
wait

# CLF="nbc_proba"

# for x in $(seq 1 $TOTAL)
# do
# 	sh two-step_depression_classification-contest_testing.sh $x $CLF $PROC &
# done

# echo "Waiting for 10 jobs to finish"
# wait

# CLF="nbc"

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p 'n'
# python3 zstats.py -m $MODE

# ERDE calculation
# sh erde_test.sh $MODE

# Cleanup
rm -r $ROOTF