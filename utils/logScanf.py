import scanf
import pandas as pd
import numpy as np
def lineScanf(line, fmt, n=None):
    """
    LINE SCAN FUNCTIONL
    line: string
    fmt: string
    n: int
    return: list
    """
    if n is None:
        return scanf.scanf(fmt, line)
    else:
        k = scanf.scanf(fmt, line)
        
        if k is not None:
            if len(k) != n:
                return None
            return k
        else:
            return None

def logScanf(log, fmt, index=None):
    """
    LOG SCAN FUNCTION
    log: string
    fmt: string
    return: list
    """
    # read
    all = []
    with open(log, 'r') as f:
        line=f.readline()
        while line:
            if index is not None:
                context = lineScanf(line, fmt, len(index))
                if context is not None:
                    all.append(context)
                    # print("done --")
            else:
                context = scanf.scanf(fmt, line)
                if context is not None:
                    all.append(context)
            line=f.readline()


    if not all:
        return None
    if index is not None:
        out = pd.DataFrame(np.array(all), columns=index)
    else:
        out = pd.DataFrame(np.array(all))
    return out
