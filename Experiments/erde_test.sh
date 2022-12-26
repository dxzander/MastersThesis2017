#!/bin/bash

RESULTS="../Results"
EVAL="../Dataset/training/scripts evaluation"
CLF="nbc"
TOTAL=10

if [ $# -eq 0 ]
then
	MODE="post_bow_ngram_ig_time_nbc_user_stats_time"
else
	MODE=$1
fi

rm "$RESULTS/results_erde.txt"

# ERDE calculation
# empty folders and refill with all 0 files
for x in A B C D
do
	rm "$RESULTS/eval/$x/"*

	for y in $(seq 1 10)
	do
		cp "$RESULTS/dummy_list.txt" "$RESULTS/eval/$x/CHEPE${x}_$y.txt"
	done
done

for x in 1 2 3 4 5 6 7 8 9 10
do
	rm "$RESULTS/eval/$x/"*

	for y in $(seq 1 10)
	do
		cp "$RESULTS/dummy_list.txt" "$RESULTS/eval/$x/${MODE}_$y.txt"
	done
done

# copy real files
cp -f "$RESULTS/CHEPEA_10.txt" "$RESULTS/eval/A/CHEPEA_10.txt"
cp -f "$RESULTS/CHEPEB_10.txt" "$RESULTS/eval/B/CHEPEB_10.txt"
cp -f "$RESULTS/CHEPEC_10.txt" "$RESULTS/eval/C/CHEPEC_3.txt"
cp -f "$RESULTS/CHEPED_10.txt" "$RESULTS/eval/D/CHEPED_5.txt"

for x in 1 2 3 4 5 6 7 8 9 10
do
	cp -f "$RESULTS/${MODE}_${x}.txt" "$RESULTS/eval/$x/"
	sed -i -e 's/\t\t0/\t\t2/g' "$RESULTS/eval/$x/${MODE}_${x}.txt"
done

# aggregate files
for x in A B C D 1 2 3 4 5 6 7 8 9 10
do
	python "$EVAL/aggregate_results.py" -path "$RESULTS/eval/$x/" -wsource "$EVAL/writings_all_test_users.txt"
done

echo "Running ERDE evaluation."

# evaluate files
for x in A B C D
do
	printf "\n$x evaluations\n"
	printf "\n$x 5 evaluation\n" >> "$RESULTS/results_erde.txt"
	python -W ignore "$EVAL/erisk_eval.py" -gpath "$EVAL/test_golden_truth.txt" -ppath "$RESULTS/eval/$x/CHEPE${x}_global.txt" -o 5 >> "$RESULTS/results_erde.txt"
	printf "\n$x 50 evaluation\n" >> "$RESULTS/results_erde.txt"
	python -W ignore "$EVAL/erisk_eval.py" -gpath "$EVAL/test_golden_truth.txt" -ppath "$RESULTS/eval/$x/CHEPE${x}_global.txt" -o 50 >> "$RESULTS/results_erde.txt"
done

for x in 1 2 3 4 5 6 7 8 9 10
do
	printf "\n$x evaluations\n"
	printf "\n$x 5 evaluation\n" >> "$RESULTS/results_erde.txt"
	python -W ignore "$EVAL/erisk_eval.py" -gpath "$EVAL/test_golden_truth.txt" -ppath "$RESULTS/eval/$x/${MODE}_global.txt" -o 5 >> "$RESULTS/results_erde.txt"
	printf "\n$x 50 evaluation\n" >> "$RESULTS/results_erde.txt"
	python -W ignore "$EVAL/erisk_eval.py" -gpath "$EVAL/test_golden_truth.txt" -ppath "$RESULTS/eval/$x/${MODE}_global.txt" -o 50 >> "$RESULTS/results_erde.txt"
done

#echo "Waiting for all evaluations to finish."
#wait