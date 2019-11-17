for p in $(seq 1 16)
do 
    for n in 1000 5000 10000 50000 100000 500000 1000000 
    do
        sbatch -J alek1 -p RT -N 1 -o "n_$n;p_$p.out" --ntasks-per-node=$p --wrap="mpirun -np ${p} python Pi.py ${n} ${p}" --exclusive
    done
done
