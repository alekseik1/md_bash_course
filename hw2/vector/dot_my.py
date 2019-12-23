from mpi4py import MPI
import numpy as np
import time
import sys

def send_parts(x, y, comm, node):
    req1 = comm.isend(x, dest=node, tag=0)
    req2 = comm.isend(y, dest=node, tag=1)
    return [req1, req2]

def sum_send(comm):
    own_x = comm.recv(source=0, tag=0)
    own_y = comm.recv(source=0, tag=1)
    comm.send(sum([own_x[i]*own_y[i] for i in range(len(own_x))]), dest=0, tag=5)


if __name__ == '__main__':

    comm = MPI.COMM_WORLD
    myrank = comm.Get_rank()
    nproc = comm.Get_size()
    n, x, y = 0, np.array([]), np.array([])
    if myrank == 0:
        n = int(sys.argv[1])
        #x, y = np.random.rand(n), np.random.rand(n)
        x, y = np.empty(n), np.empty(n)
        start_time = time.time()
        reqs = []
        for i, arr in enumerate(np.array_split(np.array([x, y]), nproc-1, axis=1)):
            reqs.extend(send_parts(arr[0, :], arr[1, :], comm, i+1))
        [req.wait() for req in reqs]
        total_sum = sum([comm.recv(source=i, tag=5) for i in range(1, nproc)])
        print(f'{n};{nproc};{time.time() - start_time}')
    else:
        sum_send(comm)

