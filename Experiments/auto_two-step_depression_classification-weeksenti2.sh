#!/bin/bash

RESULTS="../Results"
EVAL="../Dataset/training/scripts evaluation"
CLF="nbc"
PROC="weeksenti"
ROOTF=$HOME/Desktop/$PROC
MODE="post_senti_${CLF}_user_weekly_activity"
TOTAL=10
mkdir $ROOTF

# set title
echo '\033]2;Training\007'

sh two-step_depression_classification-weeksenti_training.sh $CLF $PROC

# set title
echo '\033]2;Testing\007'

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-weeksenti_testing.sh $x $CLF $PROC &
done

echo "Waiting for $TOTAL jobs to finish"
wait

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p "n"

# ERDE calculation
./erde_test.sh $MODE

# Cleanup
#rm -r $ROOTF