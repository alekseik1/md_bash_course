#!/bin/bash
if [[ $# -ne 3 ]]; then
    echo "Usage: <number 1> <number 2> <operation>"
    echo "where <operation> can be '+', '-', '*', '/' (without quotes)"
    exit 1
fi

if hash bc 2>/dev/null; then
    bc -l <<< "$1$3$2" | xargs echo
    exit 0
else
    if [[ $3 -eq '/' ]]; then
       echo "No 'bc' utility is found. Division will be integer"
    fi
    let result=$1$3$2
    echo $result
    exit 0
fi
