import numpy as np
import sys
from logger_ import setup_logger
import time


class MpiAdapter:
    def __init__(self, master_node=0):
        from mpi4py import MPI
        self.comm = MPI.COMM_WORLD
        self._MPI = MPI
        self.total_workers = self.comm.Get_size()
        self.master_node = master_node
        self.slave_nodes = list(set(range(self.comm.Get_size())) - {self.master_node})
        self.logger = setup_logger(self.comm)
        self.send_queue = []
        if self.master_node == self.comm.Get_rank():
            self.logger.info('Total processes: {}'.format(self.comm.Get_size()))
            self.logger.info('Master process: {}'.format(self.master_node))
            self.logger.info('Slave processes: {}'.format(self.slave_nodes))

    @property
    def my_id(self):
        return self.comm.Get_rank()

    @property
    def am_i_master(self):
        return self.comm.Get_rank() == self.master_node

    def send_to(self, whom, data, tag=0):
        self.comm.send(data, dest=whom, tag=tag)

    def async_send_to(self, whom, data, tag=0):
        self.send_queue.append(self.comm.isend(data, dest=whom, tag=tag))

    def wait_for_send(self):
        while True:
            if len(self.send_queue) == 0:
                return
            current_request = self.send_queue.pop()
            current_request.wait()

    def receive_from(self, source, tag=0):
        return self.comm.recv(source=source, tag=tag)


def generate_matrix(num_rows, num_columns):
    logger.info(f'Generating matrix with shape: {(num_rows, num_columns)}')
    return np.random.random((num_rows, num_columns))


def process_master(adapter: MpiAdapter):
    matrix_a = generate_matrix(num_rows=num_rows_1, num_columns=num_cols_1)
    matrix_b = generate_matrix(num_rows=num_rows_2, num_columns=num_cols_2)
    start_time = time.time()
    progress_counter = 0
    # Split matrix for all the workers
    split_a = np.array_split(matrix_a, len(adapter.slave_nodes), axis=0)
    split_b = np.array_split(matrix_b, len(adapter.slave_nodes), axis=1)
    # Send slices
    offset_row, offset_col = (0, 0)
    total_result = np.zeros((num_rows_1, num_cols_2))
    for slice_a in split_a:
        adapter.logger.debug('Iteration `slice_a`')
        all_nodes = adapter.slave_nodes.copy()
        for slice_b in split_b:
            node = all_nodes.pop()
            adapter.logger.info(f'Sending to node: {node}. Data: {(slice_a.shape, slice_b.shape)}')
            adapter.logger.info(f'About to send: {slice_a.nbytes + slice_b.nbytes} bytes')
            adapter.async_send_to(node, (slice_a, slice_b, offset_row, offset_col))
            offset_col += slice_b.shape[1]
        # NOTE: it is important to wait for send to complete since mpi4py has strange problems
        adapter.logger.info('Waiting for SEND to finish...')
        adapter.wait_for_send()
        adapter.logger.info('SEND is finished')

        adapter.logger.info(f'Waiting for results from salves...')
        # NOTE: it is important that we at first send all, and ONLY THEN wait for results
        adapter.logger.debug(f'total_result shape: {total_result.shape}')
        for node in adapter.slave_nodes[::-1]:
            # Receive
            adapter.logger.info(f'Waiting from: {node}')
            result, offset_row_received, offset_col_received = adapter.receive_from(node)
            adapter.logger.info(f'Received results: {(result.shape, offset_row, offset_col)}')
            adapter.logger.debug(f'offset_row: {offset_row} | offset_col: {offset_col} | result.shape: {result.shape}')
            total_result[
                offset_row_received:offset_row_received + result.shape[0],
                offset_col_received:offset_col_received + result.shape[1]] = result
            adapter.logger.debug(f'Updated total_result')
            progress_counter += 1
            adapter.logger.info(f'#### PROGRESS: {100*progress_counter/(len(split_a)*len(split_b))} % ####')
        offset_col = 0
        offset_row += slice_a.shape[0]
        adapter.logger.debug(f'offset_row increased')
    for slave_id in adapter.slave_nodes:
        adapter.logger.info(f'Sending finish signal to: {slave_id}')
        adapter.send_to(slave_id, ('finish',))
        adapter.logger.debug(f'Finsih singal sent to: {slave_id}')
    # logger.debug(f'Result is correct: {np.all(total_result == np.dot(matrix_a, matrix_b))}')
    if do_write_output:
        logger.info('Writing to csv file..')
        np.savetxt('result.csv', total_result, delimiter=',')
        logger.info('Written to csv')
    logger.info('Bye-bye!')
    return time.time() - start_time


def process_slave(adapter: MpiAdapter):
    while True:
        data = adapter.receive_from(adapter.master_node)
        # Signal to stop all workers
        adapter.logger.debug(f'Received message. len: {len(data)}')
        if len(data) == 1:
            adapter.logger.info(f'Received stop message. EXIT')
            return
        slice_1, slice_2, offset_row, offset_col = data
        adapter.logger.info(f'Unpacked. Shape: {(slice_1.shape, slice_2.shape)}')
        result = np.dot(slice_1, slice_2)
        adapter.logger.info(f'Finished calculating product.')
        adapter.logger.info(f'Sending back. Shape: {result.shape}')
        adapter.send_to(adapter.master_node, (result, offset_row, offset_col))
        adapter.logger.info('Send back to master')


if __name__ == '__main__':
    mpi_adapter = MpiAdapter(master_node=0)
    logger = mpi_adapter.logger
    logger.info('Process started')
    start_time = time.time()
    num_rows_1, num_cols_1, num_rows_2, num_cols_2, do_write_output = map(int, sys.argv[1:6])
    if mpi_adapter.am_i_master:
        time_elapsed = process_master(mpi_adapter)
        print(time_elapsed)
    else:
        process_slave(mpi_adapter)
    mpi_adapter._MPI.Finalize()
