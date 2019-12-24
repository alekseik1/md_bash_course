for p in $(seq 2 8)
do 
    for n in 10 20 30 40 50 60 70
    do
        sbatch -J n${n}p$p -p RT -N 1 -o "n_$n;p_$p.out" --ntasks-per-node=$p --wrap="mpirun -np ${p} python mm.py ${n} ${n}" --exclusive
    done
done
