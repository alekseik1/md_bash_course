import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
from numpy import around
import sys

if __name__ == '__main__':
    data_path = sys.argv[1]
    data = pd.read_csv(data_path, sep=';', header=None)
    slope, intercept, r_value, p_value, std_err = linregress(data)
    Mb_per_second = 1/slope/(1024*4)
    plt.title('Mb per sec: {}'.format(Mb_per_second))
    plt.scatter(data[0], data[1])
    plt.xlabel('message size')
    plt.ylabel('time, [s]')
    plt.grid()
    plt.show()

