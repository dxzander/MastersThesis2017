#!/bin/bash

RESULTS="../Results"
TOTAL=10
CLF="nbc"
MODE="${CLF}_user_time"

for x in $(seq 1 $TOTAL)
do
	sh time_only_depression_classification-time_zones.sh $x $CLF &
done
echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

CLF="nbc_proba"

for x in $(seq 1 $TOTAL)
do
	sh time_only_depression_classification-time_zones.sh $x $CLF &
done
echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

CLF="nbc"

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE
