# '''
# Author: Withoutwaxwqy 2137697992@qq.com
# Date: 2025-03-26 14:59:20
# LastEditors: Withoutwaxwqy 2137697992@qq.com
# LastEditTime: 2025-03-26 15:04:29
# FilePath: \GNSSutils\IMU\simulate\imuPosAltSim.py
# Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
# '''
import numpy as np
import matplotlib.pyplot as plt

"""
考虑零偏不稳定和随机游走的IMU误差模型
1. 零偏不稳定模型 - 一部分是随机游走模型， 一部分是维纳过程
2. 随机游走模型 - 随机游走模型

W_m = W_t + 维纳过程 + 高斯白噪声
维纳过程是值 疾风得到的角度的误差是维纳过程
维纳过程可以严格个理解为高斯白噪声的积分
"""
import numpy as np

class IMUerrorSimlator():
    """
    IMUerrorSimlator is a class to simulate IMU errors.
    Attributes:
    
    """
    def __init__(self, config):
        """
        Initialize the IMUerrorSimlator with frequency, time duration, and noise parameters.
        :param freq: frequency of the data
        :param T: time duration
        :param sigma: standard deviation of the noise
        :param sigma_w: standard deviation of the random walk
        """

        self.imufreq = config.get("freq", 100)
        # 确定性误差 
        self.accBias  = config.get("accB0", [0.0, 0.0, 0.0]) # mg
        self.gyroBias = config.get("gyroB0", [0.0, 0.0, 0.0]) # deg/s
        self.accscalefactor  = config.get("acck0", [1.0, 1.0, 1.0]) # %
        self.gyroscalefactor = config.get("gyrok0", [1.0, 1.0, 1.0]) # %
        self.accNonAlign = config.get("accN0", [0.0, 0.0, 0.0]) # %
        self.gyroNonAlign = config.get("gyroN0", [0.0, 0.0, 0.0]) # %
        # 随机误差
        self.accarw = config.get("accarw", [0.0, 0.0, 0.0]) # mg/sqrt(s)
        self.gyroarw = config.get("gyroarw", [0.0, 0.0, 0.0]) # deg/sqrt(s)
        self.accBI = config.get("accBI", [0.0, 0.0, 0.0])
        self.gyroBI = config.get("gyroBI", [0.0, 0.0, 0.0])


        # init some model parameters
        self.accmA = np.array([[self.accscalefactor[0],self.accNonAlign[0],self.accNonAlign[2],self.accBias[0]],
                               [self.accNonAlign[0],self.accscalefactor[1],self.accNonAlign[1],self.accBias[1]],
                               [self.accNonAlign[2],self.accNonAlign[1],self.accscalefactor[2],self.accBias[2]]])
        self.gyromA =  np.array([[self.gyroscalefactor[0],self.gyroNonAlign[0],self.gyroNonAlign[2],self.gyroBias[0]],
                               [self.gyroNonAlign[0],self.gyroscalefactor[1],self.gyroNonAlign[1],self.gyroBias[1]],
                               [self.gyroNonAlign[2],self.gyroNonAlign[1],self.gyroscalefactor[2],self.gyroBias[2]]])
        


def winer(T, step, mean, std):
    """
    维纳过程
    T: 总时长
    step: 步长（1s内的数据个数）
    mean: 均值
    std: 标准差
    """
    N = int(T/step)
    s = np.random.normal(mean, std, N)
    Z = np.cumsum(s)
    return Z