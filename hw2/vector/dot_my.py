from mpi4py import MPI
import numpy as np
import time
import sys

def send_parts(x, y, comm, node):
    comm.send(x, dest=node, tag=0)
    comm.send(y, dest=node, tag=1)

def sum_send(comm):
    own_x = comm.recv(source=0, tag=0)
    own_y = comm.recv(source=0, tag=1)
    comm.send(np.dot(own_x, own_y), dest=0, tag=5)


def split_vectors(x, node, nproc):
    base_length = len(x)//nproc
    lengths = [base_length]*nproc
    i = -1
    while sum(lengths) < len(x):
        lengths[i] += 1
        i -= 1
    for k in range(nproc):
        start = sum(lengths[:k])
        stop = sum(lengths[:k+1])
        yield x[start:stop], y[start:stop]


if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    myrank = comm.Get_rank()
    nproc = comm.Get_size()
    n, x, y = 0, np.array([]), np.array([])
    start_time = time.time()
    if myrank == 0:
        n = int(sys.argv[1])
        x, y = np.random.rand(n), np.random.rand(n)
        i = 0
        for x_part, y_part in split_vectors(x, y, nproc):
            send_parts(x_part, y_part, comm, i)
            i += 1
        total_sum = sum([comm.recv(source=i, tag=5) for i in range(nproc)])
    else:
        sum_send(comm)

