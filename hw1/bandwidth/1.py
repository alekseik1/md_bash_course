from mpi4py import MPI
import numpy as np
import time
import sys


if (__name__ == '__main__'):
    comm = MPI.COMM_WORLD
    myrank = comm.Get_rank()
    nproc = comm.Get_size()
    msgLen = int(sys.argv[1])
    if myrank == 0:
        a = np.arange(msgLen, dtype='i')
        comm.Bcast([a, msgLen, MPI.INT], root=0)
    else:
        a = np.zeros(msgLen, dtype='i')
        start = time.time()
        comm.Recv([a, msgLen, MPI.INT], source=0, tag=7)
        end = time.time()
        print('{} {}'.format(msgLen, end-start))

