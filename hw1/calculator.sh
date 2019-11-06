#!/bin/bash
if [[ $# -ne 3 ]]; then
    echo "Usage: <number 1> <number 2> <operation>"
    echo "where <operation> can be '+', '-', 'x' '/' (without quotes)"
    exit 1
fi

operation=$3

if [[ $3 = 'x' ]]; then
    operation=\*
fi

if hash bc 2>/dev/null; then
    bc -l <<< "$1$operation$2" | xargs echo
    exit 0
else
    if [[ $3 = '/' ]]; then
       echo "WARNING: no 'bc' utility is found. Division will be integer"
    fi
    let result=$1$operation$2
    echo $result
    exit 0
fi
