import os
import numpy as np
import pandas as pd

import re


class allan:
    def __init__(self, imufreq, mode="Standard", n=100):
        # self.data = data  ----> get data from function not from init
        self.imufreq = imufreq
        self.mode=mode
        self.tau = []
        self.sigma = []

    def allan(self, data):
        """
        Allan Variance
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

