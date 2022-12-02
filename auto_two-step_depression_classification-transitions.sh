#!/bin/bash

RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
CLF="nbc"
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_transitions"
TOTAL=10

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-transitions.sh $x $CLF &
done

echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

CLF="nbc_proba"

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-transitions.sh $x $CLF &
done

echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

CLF="nbc"

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE