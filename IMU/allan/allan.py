import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re


class allan:
    def __init__(self, imufreq, mode="Standard", n=100, **kwargs):
        
        # self.data = data  ----> get data from function not from init
        self.imufreq = imufreq
        self.mode=mode
        self.tau = [] # 3xN
        self.sigma = [] # 3xN
        self.N = np.zeros(shape=(3))
        self.B = np.zeros(shape=(3))

    def allan(self, data):
        """
        Allan Variance
        steps:
        1. comfirm the Tau (auto or manual)
        2. comfirm the mode (Standard, Overlap, half_overlap, Equal_interval)
        3. generate the Allan Variance (numba acceleration?) 
        
        """




        self.data = data
        if self.mode == "Standard":
            return self.standard_allan()
        elif self.mode == "Overlap":
            return self.overlap_allan()
        elif self.mode == "half_overlap":
            return self.half_overlap_allan()
        elif self.mode == "Equal_interval":
            return self.equal_interval_allan()
        
    def standard_allan(self):
        """
        Standard Allan Variance
        """
        y = self.data
        y = __modify_imu(y)
        y = np.array(y.tolist())
        imufreq = self.imufreq
        tau0 = 1/imufreq
        N = len(y)
        NL = N
        # calculate the standard deviation of the data
        sigma = []
        tau = []
        # calculate the Allan variance
        for k in range(1, 1000):
            sigma_k = np.sqrt(1/(2*(NL-1))*np.sum((y[1:NL]-y[0:(NL-1)])**2))
            sigma.append(sigma_k)
            tau_k = 2 ** (k-1) * tau0
            tau.append(tau_k)

            NL = int(bp.floor(NL/2))
            if NL < 3:
                break
            y = 1/2*(y[0:NL*2:2]+y[1:NL*2:2])
        self.tau = tau
        self.sigma = sigma
    
    def half_overlap_allan(self):
        """
        Half Overlap Allan Variance
        """
        y = self.data
        y = __modify_imu(y)
    
        imufreq = self.imufreq
        tau0 = 1/imufreq
        N = len(y)
        NL = N
        # calculate the standard deviation of the data
        sigma = []
        tau = []
        # calculate the Allan variance
        for k in range(1, 1000):
            sigma_k = np.sqrt(1/(2*(NL-1))*np.sum((y[1:NL]-y[0:(NL-1)])**2))
            sigma.append(sigma_k)
            tau_k = 2 ** (k-1) * tau0
            tau.append(tau_k)

            NL = int(bp.floor(NL/2))
            if NL < 3:
                break
            y = 1/2*(y[0:NL*2:2]+y[1:NL*2:2])
        self.tau = tau
        self.sigma = sigma


    def overlap_allan(self):
        """
        Overlap Allan Variance
        """
        y = self.data
        y = __modify_imu(y)
        imufreq = self.imufreq
        tau0 = 1/imufreq
        N = len(y)
        NL = N
        # calculate the standard deviation of the data
        sigma = []
        tau = []
        # calculate the Allan variance
        for k in range(1, 1000):
            sigma_k = np.sqrt(1/(2*(NL-1))*np.sum((y[1:NL]-y[0:(NL-1)])**2))
            sigma.append(sigma_k)
            tau_k = 2 ** (k-1) * tau0
            tau.append(tau_k)

            NL = int(bp.floor(NL/2))
            if NL < 3:
                break
            y = 1/2*(y[0:NL*2:2]+y[1:NL*2:2])
        self.tau = tau
        self.sigma = sigma


    def calculate_index(self):
        """
        Calculate the index
        N: angle random walk
        B: bias instability
        
        there also several methods to calculate the index

        """
        pass

    def plot_allan_GYR(self, unit=3600, xscalelim=[1, 1000],yscalelim=[0.1,100],savepath=None):
        """
        plot the Allan Variance of Gyroscope in loglog
        """
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        RGBlist = ["r", "g", "b"]
        for i in range(3):
            ax.loglog(self.tau[i, :], self.sigma[i, :]*unit, label="Allan Variance", color = RGBlist[i])
        ax.set_xlabel("Tau (s)")
        ax.set_ylabel("Allan Standard deviation [deg/h]")
        ax.set_title("Gyroscope -- Allan Variance")
        ax.grid(True, which="both", ls="--")
        ax.set_xlim((xscalelim[0], xscalelim[1]))
        ax.set_ylim((yscalelim[0], yscalelim[1]))
        ax.legend(["GyroX", "GyroY", "GyroZ"])

        if savepath is not None:
            plt.savefig(savepath, dpi=300)
        else:
            plt.show()


    def plot_allan_ACC(self, unit=1e6, xscalelim=[1, 1000],yscalelim=[1, 1000],savepath=None):
        """
        plot the Allan Variance of Gyroscope in loglog
        """
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        RGBlist = ["r", "g", "b"]
        for i in range(3):
            ax.loglog(self.tau[i, :], self.sigma[i, :]*unit, label="Allan Variance", color = RGBlist[i])
            # if self.N and self.B exist  plot auxiliary line
            if self.N[0] != 0:
                x_aux = np.logspace(1, 3, 100)
                y_N_au = np.power(10, self.N[i]+0.5)*np.power(x_aux, -0.5)
                y_B_au = np.power(10, self.B[i])*np.ones_like(x_aux)
                ax.loglog(x_aux, y_N_au, ":", color = RGBlist[i])
                ax.loglog(x_aux, y_B_au, "--", color = RGBlist[i])
                


        ax.set_xlabel("Tau (s)")
        ax.set_ylabel("Allan Standard deviation [ug]")
        ax.set_title("Accelerometer -- Allan Variance")
        ax.grid(True, which="both", ls="--")
        ax.set_xlim((xscalelim[0], xscalelim[1]))
        ax.set_ylim((yscalelim[0], yscalelim[1]))
        ax.legend(["AcceX", "AcceY", "AcceZ"])

        if savepath is not None:
            plt.savefig(savepath, dpi=300)
        else:
            plt.show()



def __modify_imu(data):
    if np.ndim(data) == 1:
        data = np.array(data.tolist())
    if np.ndim(data) == 2:
        if data.shape[0] > 100 and data.shape[1] == 6:
            data = data
        elif data.shape[0] == 6 and data.shape[1] > 100:
            data = data.T
        elif data.shape[0] == 7 and data.shape[1] == 100:
            data = data[1:, :]
            data = data.T
        elif data.shape[0] == 100 and data.shape[1] == 7:
            data = data[:, 1:]
        else:
            raise ValueError("IMU data error! Please check the input data.should be [Time* GYRX Y Z ACCX Y Z] (Time optional)")
    return data

