from mpi4py import MPI
import sys
import numpy as np
import time

number_rows = int(sys.argv[1])
number_columns = int(sys.argv[2])
TASK_MASTER = 0


# print("Initialising variables.\n")
a = np.zeros(shape=(number_rows, number_columns))
b = np.zeros(shape=(number_rows, number_columns))
c = np.zeros(shape=(number_rows, number_columns))


def populate_matrix(matrix, num_rows, num_columns):
    """
    Populates both matrices with values
    """
    for i in range(0, num_rows):
        for j in range(0, num_columns):
            matrix[i][j] = i + j


# Initialize MPI
comm = MPI.COMM_WORLD
world_size = comm.Get_size()
rank = comm.Get_rank()
processorName = MPI.Get_processor_name()
##################################################

# print("Process %d started.\n" % rank)
# print("Running from processor %s, rank %d out of %d processors.\n" % (processorName, rank, world_size))

# Calculate the slice per worker
if world_size == 1:
    slice_size = number_rows
else:
    slice_size = int(number_rows / (world_size - 1))    # make sure it is divisible

assert slice_size >= 1


comm.Barrier()
    
if rank == TASK_MASTER:
    # print("Initialising Matrix A (%d,%d).\n" % (number_rows, number_columns))
    populate_matrix(a, num_rows=number_rows, num_columns=number_columns)
    # print("Initialising Matrix A (%d,%d).\n" % (number_rows, number_columns))
    populate_matrix(b, num_rows=number_rows, num_columns=number_columns)
    # print("Start")
    start_time = time.time()

    for i in range(1, world_size):
        offset = int((i-1) * slice_size)    # 0, 10, 20
        row = a[offset,:]
        comm.send(offset, dest=i, tag=i)
        comm.send(row, dest=i, tag=i)
        for j in range(0, slice_size):
            comm.send(a[j+offset,:], dest=i, tag=j+offset)
    #print ("All sent to workers.\n")

comm.Barrier()

if rank != TASK_MASTER:
    # print("Data Received from process %d.\n" % rank)
    offset = comm.recv(source=0, tag=rank)
    recv_data = comm.recv(source=0, tag=rank)
    for j in range(1, slice_size):
        c = comm.recv(source=0, tag=j+offset)
        recv_data = np.vstack((recv_data, c))

    # print("Start Calculation from process %d.\n" % rank)

    # Loop through rows
    t_start = MPI.Wtime()
    for i in range(0, slice_size):
        res = np.zeros(shape=(number_columns))
        if slice_size == 1:
            r = recv_data
        else:
            r = recv_data[i,:]
        ai = 0
        for j in range(0, number_columns):
            q = b[:,j]  # get the column we want
            for x in range(0, number_columns):
                res[j] = res[j] + (r[x]*q[x])
            ai = ai + 1
        if i > 0:
           send = np.vstack((send, res))
        else:
            send = res
    t_diff = MPI.Wtime() - t_start
    
    # print("Process %d finished in %5.4fs.\n" %(rank, t_diff))
    # Send large data
    # print ("Sending results to Master %d bytes.\n" % (send.nbytes))
    comm.Send([send, MPI.FLOAT], dest=0, tag=rank) #1, 12, 23

comm.Barrier()

if rank == TASK_MASTER:  
    #print ("Checking response from Workers.\n")
    res1 = np.zeros(shape=(slice_size, number_columns))
    comm.Recv([res1, MPI.FLOAT], source=1, tag=1)
    #print ("Received response from 1.\n")
    kl = np.vstack((res1))
    for i in range(2, world_size):
        resx= np.zeros(shape=(slice_size, number_columns))
        comm.Recv([resx, MPI.FLOAT], source=i, tag=i)
        #print ("Received response from %d.\n" % (i))
        kl = np.vstack((kl, resx))
    # print("End")
    print(time.time() - start_time)
    #print ("Result AxB.\n")
    #print (kl)   

comm.Barrier()

MPI.Finalize()
