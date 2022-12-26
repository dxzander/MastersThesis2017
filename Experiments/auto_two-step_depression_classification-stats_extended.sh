#!/bin/bash

RESULTS="../Results"
CLF="nbc"
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_time_extended"
TOTAL=10
for x in $(seq 1 $TOTAL)
do
	#xterm -e sh two-step_depression_classification.sh $x &
	sh two-step_depression_classification-stats_extended.sh $x &
done

echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

echo "Getting results"
#python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE