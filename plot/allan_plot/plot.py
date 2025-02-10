'''
Author: Withoutwaxwqy 2137697992@qq.com
Date: 2025-02-06 11:00:02
LastEditors: Withoutwaxwqy 2137697992@qq.com
LastEditTime: 2025-02-06 11:24:15
FilePath: \GNSSutils\plot\allan_plot\plot.py
Description: IMU Allan Variance plot
'''

import matplotlib.pyplot as plt

def plotAllanGYR(avar, tau, index, unit=3600, xscale=[1, 1000], yscale=[1e-1, 1e2], freq=100,
                 savepath=None):
    """
    plot 3 axis gyroscope Allan Variance in one figure
        * avar: Allan Variance should be 3xN array
        * tau: time interval  should be 3xN array
        * unit: unit of the data (e.g. 3600 for deg/h, 1 for deg/s)
    """
    RGBlist = ["red", "green", "blue"]
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # plot every axis
    for i in range(3):

        avar0 = avar[i, :]*unit
        tau0 = tau[i, :]
        ax.loglog(tau0, avar0, label="Allan Variance", color = RGBlist[i])

    # beautify the plot 
    ax.set_xlabel("Tau (s)")
    if unit == 3600:
        ax.set_ylabel("Allan Variance [deg/h]")
    elif unit == 1:
        ax.set_ylabel("Allan Variance [deg/s]")
    ax.set_xlim((xscale[0], xscale[1]))
    ax.set_ylim((yscale[0], yscale[1]))
    ax.set_title("Gyroscope -- Allan Variance")
    ax.grid(True, which="both", ls="--")
    ax.legend(index)
    if savepath is not None:
        plt.savefig(savepath, dpi=300)
    else:
        plt.show()


def plotAllanACC(avar, tau, index, unit=1e6, xscale=[1, 1000], yscale=[1e-2, 1e3], freq=100,
                 savepath=None):
    """
    plot 3 axis accelerometer Allan Variance in one figure
        * avar: Allan Variance should be 3xN array
        * tau: time interval  should be 3xN array
        * unit: unit of the data (e.g. 1 for m/s^2)
    """
    RGBlist = ["red", "green", "blue"]
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # plot every axis
    for i in range(3):

        avar0 = avar[i, :]*unit
        tau0 = tau[i, :]
        ax.loglog(tau0, avar0, label="Allan Variance", color = RGBlist[i])

    # beautify the plot 
    ax.set_xlabel("Tau (s)")
    ax.set_ylabel("Allan Variance [ug]")
    ax.set_xlim((xscale[0], xscale[1]))
    ax.set_ylim((yscale[0], yscale[1]))
    ax.set_title("Accelerometer -- Allan Variance")
    ax.grid(True, which="both", ls="--")
    ax.legend(index)
    if savepath is not None:
        plt.savefig(savepath, dpi=300)
    else:
        plt.show()


def plotMultiAllanGYR(avar, tau, index, unit=3600, xscale=[1, 1000], yscale=[1e-1, 1e2], freq=100,
                 savepath=None):
    """
    plot multiple gyroscope Allan Variance in one figure
        * avar: Allan Variance should be 3xN array
        * tau: time interval  should be 3xN array
        * unit: unit of the data (e.g. 3600 for deg/h, 1 for deg/s)
    """
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # plot every axis
    for i in range(len(index)):

        avar0 = avar[i, :]*unit
        tau0 = tau[i, :]
        ax.loglog(tau0, avar0, label="Allan Variance")

    # beautify the plot 
    ax.set_xlabel("Tau (s)")
    if unit == 3600:
        ax.set_ylabel("Allan Variance [deg/h]")
    elif unit == 1:
        ax.set_ylabel("Allan Variance [deg/s]")
    ax.set_xlim((xscale[0], xscale[1]))
    ax.set_ylim((yscale[0], yscale[1]))
    ax.set_title("Gyroscope -- Allan Variance")
    ax.grid(True, which="both", ls="--")
    ax.legend(index)
    if savepath is not None:
        plt.savefig(savepath, dpi=300)
    else:
        plt.show()



def plotMultiAllanACC(avar, tau, index, unit=1e6, xscale=[1, 1000], yscale=[1e-2, 1e3], freq=100,
                 savepath=None):
    """
    plot multiple accelerometer Allan Variance in one figure
        * avar: Allan Variance should be 3xN array
        * tau: time interval  should be 3xN array
        * unit: unit of the data (e.g. 1 for m/s^2)
    """
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111)

    # plot every axis
    for i in range(len(index)):

        avar0 = avar[i, :]*unit
        tau0 = tau[i, :]
        ax.loglog(tau0, avar0, label="Allan Variance")

    # beautify the plot 
    ax.set_xlabel("Tau (s)")
    ax.set_ylabel("Allan Variance [ug]")
    ax.set_xlim((xscale[0], xscale[1]))
    ax.set_ylim((yscale[0], yscale[1]))
    ax.set_title("Accelerometer -- Allan Variance")
    ax.grid(True, which="both", ls="--")
    ax.legend(index)
    if savepath is not None:
        plt.savefig(savepath, dpi=300)
    else:
        plt.show()