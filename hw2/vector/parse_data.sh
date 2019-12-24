if [[ ! -f "results.csv" ]]; then
    echo "n;p;time" > results.csv
fi

for p in $(seq 2 8)
do 
    #for n in 1000000 5000000 10000000 50000000 100000000
    for n in 1000000 2000000 3000000 4000000 5000000 6000000 7000000 
    do
        time=$(cat "n_$n;p_${p}.out" | grep -v "-")
        echo "$time" >> results.csv
    done
done
