#!/bin/bash

RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
TOTAL=10
CLF="nbc"
MODE="${CLF}_user_bow_ngram_ig"

for x in $(seq 1 $TOTAL)
do
	sh bow_depression_classification-basic.sh $x $CLF &
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