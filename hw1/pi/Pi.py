from mpi4py import MPI
import numpy as np
import sys
import time

comm = MPI.COMM_WORLD
myrank = comm.Get_rank()
nproc = comm.Get_size()
PI25DT = 3.141592653589793238462643
n, p = 0, 0
if myrank == 0:
    n = int(sys.argv[1])
    p = int(sys.argv[2])

start = time.time()

n = comm.bcast(n, root = 0)
h = 1.0 / float(n)
sum = 0.0
i = myrank + 1
while i <= n:
	x = h * (float(i) - 0.5)
	sum += 4.0 / (1.0 + x*x)
	i += nproc
mypi = h * sum
tot_sum = 0.0
tot_sum = comm.reduce(mypi, op=MPI.SUM, root=0)
end = time.time()
if myrank == 0:
    print(f'{p};{n};{end-start}')
    # print("pi is approximately {0}\n".format(tot_sum))
    # print("error is {0}\n".format(abs(PI25DT-tot_sum)))
    # print(myrank, end - start)

