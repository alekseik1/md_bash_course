import logging
from mpi4py import MPI


class ProcessFilter(logging.Filter):
    def __init__(self, comm):
        super().__init__()
        self.comm = comm

    def filter(self, record: logging.LogRecord) -> int:
        record.rank = self.comm.Get_rank()
        return True


def setup_logger(comm):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - proc_%(rank)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addFilter(ProcessFilter(comm))
    return logger


