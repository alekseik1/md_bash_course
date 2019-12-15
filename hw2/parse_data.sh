if [[ ! -f "results.csv" ]]; then
    echo "n;p;time" > results.csv
fi

for p in $(seq 2 15)
do 
    for n in 30 60 80
    do
        time=$(cat "n_$n;p_${p}.out" | grep -v "-")
        echo "$n;$p;$time" >> results.csv
    done
done
