if [[ ! -f "results.csv" ]]; then
    echo "n;p;time" > results.csv
fi

for p in $(seq 2 8)
do 
    for n in 10 20 30 40 50 60 70
    do
        time=$(cat "n_$n;p_${p}.out" | grep -v "-")
        echo "$n;$p;$time" >> results.csv
    done
done
