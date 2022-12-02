#!/bin/bash

RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
EVAL="$HOME/ownCloud/Maestría/Datasets/reddit-depression/training/scripts evaluation"
CLF="nbc"
MODE="post_senti_${CLF}_user_stats_time"
TOTAL=10

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-sentiment2.sh $x $CLF &
done

echo "Waiting for $TOTAL jobs to finish"
wait

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p "n"

# ERDE calculation
./erde_test.sh $MODE