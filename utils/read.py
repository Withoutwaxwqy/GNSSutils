import pandas as pd
import numpy as np

def readMultiCsv(files):
    """
    READ MULTI CSV
    files: list
    return: list
    """
    all = []
    for f in files:
        data = pd.read_csv(f)
        all.append(data)
    all = pd.concat(all)
    return all