'''
Author: Withoutwaxwqy 2137697992@qq.com
Date: 2025-05-15 21:23:22
LastEditors: Withoutwaxwqy 2137697992@qq.com
LastEditTime: 2025-05-18 17:01:24
FilePath: \GNSSutils\IMU\spec\TempParaCal.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
import utils.tools as tools
import numpy as np
def CalTempPara(data, temp, freq):
    """
    Calculate temperature parameters from the given data.
    :param data: numpy array of imu data
    :param temp: numpy array of temperature values
    """

    # 取最大的上升段
    start_index, end_index, max_rise = tools.calculate_max_rising_segment(temp)
    data = data[start_index:end_index]
    temp = temp[start_index:end_index]
    
    # 计算常温的位置
    normal_temp_index = tools.find_closest_index(temp, 25)

    # 计算温度的常温零偏
    normal_temp_imu_zero_bias = np.mean(data[normal_temp_index:normal_temp_index+freq*1*60]) 
    
    # 计算10s std 零偏温漂
    data_10s_smooth = tools.filter_ns(data, 10, 100)
    All_temp_10s_zero_bias = np.std(data_10s_smooth)

    # 计算峰峰值
    datapeakpeak =  np.max(data) - np.min(data)

    return normal_temp_imu_zero_bias, All_temp_10s_zero_bias, datapeakpeak