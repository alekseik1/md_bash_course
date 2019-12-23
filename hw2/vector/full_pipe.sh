#!/bin/bash
for i in $(seq 1 10)
do
    bash run.sh
    echo Waiting for results...
    echo Running $i of 10
    bash wait_results.sh
    echo Results are ready, combining
    echo Running $i of 10
    bash parse_data.sh
    echo Done combining!
done