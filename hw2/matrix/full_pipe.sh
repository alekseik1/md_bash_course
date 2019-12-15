#!/bin/bash
for i in $(seq 1 10)
do
    bash run.sh && bash wait_results.sh && bash parse_data.sh
done
