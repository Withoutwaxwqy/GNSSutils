'''
Author: Withoutwaxwqy 2137697992@qq.com
Date: 2025-02-06 11:35:02
LastEditors: Withoutwaxwqy 2137697992@qq.com
LastEditTime: 2025-02-06 11:35:30
FilePath: \GNSSutils\plot\IMU_plot\plot.py
Description: plot related to IMU data
'''

import matplotlib.pyplot as plt
from matplotlib import rc
rc("mathtext", default="regular")

def plottempIMU(temp, data, index, path=None):
    """
    plot temperature and IMU data in different color (double axis)
    """
    fig = plt.figure(figsize=(20, 5))
    ax = fig.add_subplot(111)
    l = [i for i in range(data.shape[0])]
    ax.plot(l, data, label=index)
    ax2 = ax.twinx()
    ax2.plot(l, temp, '-r', label="Temperature")
    ax2.set_ylabel("Temperature ($^\circ$C)")
    ax.set_xlabel("Time (s)")
    ax.set_title(index)

    if path is not None:
        plt.savefig(path, dpi=300)
    else:
        plt.show()

def IMUsubplot(data, index, ylim=[5,5,5, 2,2,2], path=None):
    """
    plot IMU data in different subplots
        * data: N * 6 array 
        * index: list of the data name
        * ylim: [gyro Y limit, acc Y limit] 
    """
    fig, ax = plt.subplots(3, 2, figsize=(12, 6), sharex=True)
    l = [i for i in range(data.shape[0])]
    for i in range(3):
        for j in range(2):
            ax[i][j].plot(l, data[:, i+j*3])
            ax[i][j].set_ylabel(index[i+j*3])
            ax[i][j].set_ylim(-ylim[j], ylim[j])
    if path is not None:
        plt.savefig(path, dpi=300)
    else:
        plt.show()