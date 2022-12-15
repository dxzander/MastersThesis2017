#!/bin/bash

CLF="nbc"
PROC="contest"
RESULTS="$HOME/ownCloud/Maestría/Proyectos/depression reddit/results"
PCLAS="$RESULTS/model_${PROC}_${CLF}_post.pkl"
UCLAS="$RESULTS/model_${PROC}_${CLF}_user.pkl"
HIST="$RESULTS/histogram_${PROC}_post.pkl"
TOKH="$RESULTS/tokens_${PROC}_user.pkl"

# POST LEVEL
printf "\nPost-Level Relevant Features Extraction - $CLF\n"
python3 zmif.py -r "$RESULTS" -t "$HIST" -i "$PCLAS"

# USER LEVEL
#printf "\nUser-Level Relevant Features Extraction - $CLF\n"
#python3 zmif.py -r "$RESULTS" -t "$TOKH" -i "$UCLAS"