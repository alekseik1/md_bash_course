for p in $(seq 2 15)
do 
    for n in 30 60 80
    do
        sbatch -J n${n}p$p -p RT -N 1 -o "n_$n;p_$p.out" --ntasks-per-node=$p --wrap="mpirun -np ${p} python mm.py ${n} ${n}" --exclusive
    done
done
