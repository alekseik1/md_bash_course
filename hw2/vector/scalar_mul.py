from mpi4py import MPI
import sys
import time
import random


def scalar_mult(slice_length, vec_a, vec_b):
    result = 0
    for i in range(slice_length):
        result += vec_a[i] * vec_b[i]
    return result


if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    my_rank = comm.Get_rank()
    n_proc = comm.Get_size()
    n = 0
    if my_rank == 0:
        n = int(sys.argv[1])
    n = comm.bcast(n, root=0)
    n1 = n // n_proc
    if my_rank < n - n1 * n_proc:
        n1 += 1

    a = [0 for i in range(n1)]
    b = [0 for i in range(n1)]
    random.seed(0)
    for i in range(n1):
        a[i] = random.random()
        b[i] = random.random()
    if my_rank == 0:
        start = time.time()
    sc = scalar_mult(n1, a, b)
    globalsc = comm.reduce(sc, op=MPI.SUM, root=0)
    if my_rank == 0:
        end = time.time()
        print(f'{n_proc};{end - start}')
        print("Result = ", globalsc, " powered on ", n_proc, " proc")
        print("Time = ", end - start)
