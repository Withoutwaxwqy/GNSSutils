from utils.logScanf import logScanf


def deepLscenedetectTest(logpath):
    """
    DEEP LSCENE DETECT TEST
    log: string
    return: list
    """
    data = logScanf(logpath, 
                   "[T Debug] time:%d,cycleSlipratio:%f,average CN0:%f,average Elevation:%f,vis satellite number:%d,hDop:%f,pDop:%f,ValidLNum:%d, aveEleOfValid:%f]")
    
