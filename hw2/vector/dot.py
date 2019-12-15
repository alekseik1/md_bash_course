from mpi4py import MPI
import numpy as np
import sys
import time

comm = MPI.COMM_WORLD
myrank = comm.Get_rank()
nproc = comm.Get_size()
n = 0
x = []
y = []
p = 0
proc = 0
if myrank == 0:
    x=[]
    y=[]
    n = int(sys.argv[1])
    for i in range(n):
        x.append(np.random.randn())
        y.append(np.random.randn())
    p = round(n/(nproc-1))
start = time.time()
x = comm.bcast(x, root = 0)
y = comm.bcast(y, root = 0)
p = comm.bcast(p, root = 0)
sum = 0.0
proc = myrank
if proc == 0:
    i = p*(proc-1)
else:
    i = 0
while i < proc*p:
    sum += x[i]*y[i]
    i+=1
end = time.time()
if myrank == 0:
    print(sum, end - start)

