#!/bin/bash

RESULTS="../Results"
TOTAL=10
MODE="user_week_activity"

for x in $(seq 1 $TOTAL)
do
	sh weekly_activity_classification-correlation.sh $x &
done
echo "Waiting for $TOTAL jobs to finish"
wait %1 %2 %3 %4 %5 %6 %7 %8 %9 %10

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p 'n'
