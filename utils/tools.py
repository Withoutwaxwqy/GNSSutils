import numpy as np
def calculate_max_rising_segment(data):
    """
    Calculate the maximum rising segment in the given data.
    :param data: list or numpy array of numerical data
    :return: start_index, end_index, max_rise
    """
    max_rise = 0
    current_rise = 0
    start_index = 0
    temp_start = 0
    end_index = 0

    for i in range(1, len(data)):
        diff = data[i] - data[i - 1]
        if diff > 0:
            current_rise += diff
            if current_rise > max_rise:
                max_rise = current_rise
                start_index = temp_start
                end_index = i
        else:
            current_rise = 0
            temp_start = i

    return start_index, end_index, max_rise


def filter_ns(data, n, freq):
    """
    Filter the data using a moving average filter.
    filter data shape :[N - n*freq]
    :param data: numpy array of data to be filtered
    :param n: number of points to average over
    :param freq: frequency of the data
    :return: filtered data
    """
    # Calculate the moving average using a simple box filter
    kernel = np.ones(n*freq) / (n*freq)
    filtered_data = np.convolve(data, kernel, mode='valid')
    
    return filtered_data

def average_every_n(data, n):
    """
    Average every n points in the data.
    :param data: numpy array of data to be averaged
    :param n: number of points to average over
    :return: averaged data
    """
    # Calculate the average of every n points
    averaged_data = np.mean(data.reshape(-1, n), axis=1)
    
    return averaged_data


def find_closest_index(data, N):
    """
    Find the index of the element in the array that is closest to N.
    :param data: numpy array of numerical data
    :param N: numerical value to find the closest element to
    :return: int, index of the closest element
    """
    # 计算每个元素与 N 的绝对差值
    diff = np.abs(data - N)
    # 找到最小差值的索引
    closest_index = np.argmin(diff)
    return closest_index


