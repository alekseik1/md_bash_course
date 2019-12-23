export MKL_NUM_THREADS=1
for p in $(seq 2 8)
do 
    for n in 1000000 5000000 10000000 50000000 100000000
    do
        sbatch -J n${n}p$p -p RT -N 1 -o "n_$n;p_$p.out" --ntasks-per-node=$p --wrap="mpirun -np ${p} python dot_my.py $n" --exclusive
    done
done
