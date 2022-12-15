#!/bin/bash

RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
EVAL="$HOME/ownCloud/Maestría/Datasets/reddit-depression/training/scripts evaluation"
CLF="nbc"
PROC="contest"
ROOTF=$HOME/Desktop/$PROC
MODE="post_bow_ngram_ig_time_${CLF}_user_stats_time"
TOTAL=10
mkdir $ROOTF

# set title
echo '\033]2;Training\007'

sh two-step_depression_classification-contest_training.sh $CLF $PROC