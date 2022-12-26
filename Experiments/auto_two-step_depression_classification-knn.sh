#!/bin/bash

RESULTS="../Results"
TOTAL=10
CLF="knn"
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_time"

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-knn.sh $x $CLF &
done
echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p 'n'