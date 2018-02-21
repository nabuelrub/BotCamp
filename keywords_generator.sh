#!/bin/bash

MYPWD=${PWD}
listen_time=10800
#listen_time=600
cd $MYPWD/trends/data
mkdir $1
#night = 1
for night in {1..100}
do
cd $MYPWD/trends/data/$1
mkdir "Round_$night"
cd ..
cd ..
echo "${1}/Round_$night"
echo "find trends"
python "$MYPWD/trends/get_trends.py" "$MYPWD/trends/data/${1}/Round_$night"
echo "Listen to trends"
python "$MYPWD/trends/collector.py" 1 $listen_time "$MYPWD/trends/data/${1}/Round_$night"
echo "parsing "
python "$MYPWD/trends/parsing.py" "$MYPWD/trends/data/${1}/Round_$night" $MYPWD

done


