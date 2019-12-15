#!/bin/bash
while true
do
    left=$(squeue | grep stud | wc -l)
    if [ $left -le 0 ]
    then
        break
    fi
done
