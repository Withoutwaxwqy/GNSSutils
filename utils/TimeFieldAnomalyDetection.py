import os,sys
import numpy as np

class TimeFieldAnomalyDetector:
    def __init__(self, window_size=2, freq=100, use_line=None):
        """
        Initialize the TimeFieldAnomalyDetector with data and frequency.
        :param data: list or numpy array of numerical data
        :param freq: frequency of the data
        """
        self.window_size = window_size
        self.freq = freq
        self.use_line = use_line
        self.detect_method = "3sigma"
        self.repair_method = "linear"

    def set_Detect_Method(self, method):
        """
        Set the detection method.
        :param method: detection method
        """
        self.detect_method = method
    
    def set_Repair_Method(self, method):
        """
        Set the repair method.
        :param method: repair method
        """
        self.repair_method = method
    