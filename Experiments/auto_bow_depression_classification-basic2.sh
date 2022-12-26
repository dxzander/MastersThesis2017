#!/bin/bash

RESULTS="../Results"
EVAL="../Dataset/training/scripts evaluation"
CLF="nbc"
PROC="basic"
TOTAL=10
ROOTF=$HOME/Desktop/$PROC
MODE="${CLF}_user_bow_ngram_ig"
mkdir $ROOTF

# set title
echo '\033]2;Training\007'

sh bow_depression_classification-basic_training.sh $CLF $PROC

# set title
echo '\033]2;Testing\007'

for x in $(seq 1 $TOTAL)
do
	sh bow_depression_classification-basic_testing.sh $x $CLF $PROC &
done
echo "Waiting for $TOTAL jobs to finish"
wait

#CLF="nbc_proba"

#for x in $(seq 1 $TOTAL)
#do
#	sh bow_depression_classification-basic.sh $x $CLF &
#done
#echo "Waiting for $TOTAL jobs to finish"
#wait

#CLF="nbc"

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p "n"

# ERDE calculation
#./erde_test.sh $MODE

# Cleanup
rm -r $ROOTF