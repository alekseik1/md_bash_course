for p in 1 2 3 4 5 6 7 
do 
    for n in 1000 10000 100000 1000000 
    do
        sbatch -J alek1 -p RT -N 1 -o "n_$n;p_$p.out" --ntasks-per-node=$p --wrap="mpirun -np ${p} python Pi2_.py ${n} ${p}" --exclusive
    done
done
