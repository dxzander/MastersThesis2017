#!/bin/bash

RESULTS="../Results"
EVAL="../Dataset/training/scripts evaluation"
CLF="nbc"
MODE="post_bow_ngram_ig_time_senti_${CLF}_user_stats_time"
TOTAL=10

for x in $(seq 1 $TOTAL)
do
	#xterm -e sh two-step_depression_classification.sh $x &
	sh two-step_depression_classification-sentiment.sh $x $CLF &
done

echo "Waiting for $TOTAL jobs to finish"
wait

CLF="nbc_proba"

for x in $(seq 1 $TOTAL)
do
	#xterm -e sh two-step_depression_classification.sh $x &
	sh two-step_depression_classification-sentiment.sh $x $CLF &
done

echo "Waiting for $TOTAL jobs to finish"
wait

CLF="nbc"

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE

# ERDE calculation
./erde_test.sh $MODE