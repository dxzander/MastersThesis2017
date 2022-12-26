#!/bin/bash

CLF="nbc"
PROC="combo"
ROOTF=$HOME/Desktop/$PROC
DATA="../Dataset"
RESULTS="../Results"
MODE="user_stats_time_weekly_activity_${CLF}"
EVAL="../Dataset/training/scripts evaluation"
CLAS="$RESULTS/model_${PROC}_${CLF}_post.pkl"
TPROC="time"
WPROC="weekly"
TOTAL=10
PART=100
mkdir $HOME/Desktop/$TPROC
mkdir $HOME/Desktop/$WPROC
mkdir $HOME/Desktop/$PROC

### trainings

# set title
echo '\033]2;Training\007'

sh two-step_depression_classification-contest_training.sh $CLF $TPROC &
sh two-step_depression_classification-weeksenti_training.sh $CLF $WPROC &

echo "Waiting for both trainings"
wait

## juntar vectores y entrenar

# initialization
printf 'Initializing\n'
CNKF=$ROOTF/train
TMP=$CNKF/tmp
VAR=$CNKF/var
TRAIN=$VAR/train.txt
TEST=$VAR/test.txt
mkdir $CNKF
mkdir $TMP
mkdir $VAR
echo $MODE > $VAR/mode.txt
echo $DATA > $VAR/data.txt
python3 zinit.py -v $VAR -i $TRAIN -o $TEST

# combine
printf 'Combining vectors\n'
python3 zcombo.py -0 $HOME/Desktop/$PROC -1 $HOME/Desktop/$TPROC -2 $HOME/Desktop/$WPROC -c "train"

# classify
printf "\nCombined Training - $CLF\n"
python3 zclf.py -m 'train' -k $CLF -n $PART -i $TRAIN -o "$CLAS"

## testings

# set title
echo '\033]2;Testing\007'

# contest

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-contest_testing.sh $x $CLF $TPROC &
done

echo "Waiting for $TOTAL jobs to finish"
wait

# weekly activity

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-weeksenti_testing.sh $x $CLF $WPROC &
done

echo "Waiting for $TOTAL jobs to finish"
wait

# juntar vectores y clasificar

for x in $(seq 1 $TOTAL)
do
	sh two-step_depression_classification-combined_testing.sh $x $CLF $PROC $TPROC $WPROC &
done

echo "Waiting for $TOTAL jobs to finish"
wait

### obtener resultados

echo "Getting results"
python3 zdec.py -m $MODE -r "$RESULTS" -c $TOTAL
python3 zstats.py -m $MODE -p 'n'

# ERDE calculation
sh erde_test.sh $MODE

# Cleanup
rm -r $HOME/Desktop/$TPROC
rm -r $HOME/Desktop/$WPROC
rm -r $HOME/Desktop/$PROC