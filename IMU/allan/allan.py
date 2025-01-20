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
        elif self.mode == "Equal_interval":
            return self.equal_interval_allan()
        
    def standard_allan(self):
        """
        Standard Allan Variance
        """
        y = self.data
        if np.ndim(y) == 1:
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

        if np.ndim(y) == 2:
            if y.shape[0] > 100 and y.shape[1] == 6:
                y = y
            elif y.shape[0] == 6 and y.shape[1] > 100:
                y = y.T
            elif y.shape[0] == 7 and y.shape[1] == 100:
                y = y[1:, :]
                y=y.T
            elif y.shape[0] == 100 and y.shape[1] == 7:
                y = y[:, 1:]
            else:
                raise ValueError("IMU data error! Please check the input data.should be [Time* GYRX Y Z ACCX Y Z] (Time optional)")
            for i in range(6):
                yy = y[:, i]
                