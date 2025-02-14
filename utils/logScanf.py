import scanf
import pandas as pd
import numpy as np
import os,sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.jsonConvert import read_json_to_dict, sceneChinese2English, sliceTime

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


def quectelRootGetTraceAndJson(root):
    """
    QUECTEL ROOT GET LOG AND JSON
    root: string
    return: list, list
    """
    log_file = []
    json_file = None
    files = os.listdir(root)
    if "REPORT.json" in files:
        json_file = os.path.join(root, "REPORT.json")
    
    for f in files:
        if ".trace" in f:
            log_file.append(os.path.join(root, f))

    if len(log_file) ==0:
        print("No log file found!")
        return None, None
    
    return log_file, json_file


def trace2csv(filedict, fmt, index, save_path):
    """
    TRACE TO CSV
        * log: string
        * fmt: string
    return: list
    """
    count = 0
    for each in filedict.keys():
        # read time information from json
        scene_time = read_json_to_dict(filedict[each]["json"])
        scene_time = scene_time["Time"]
        scene_time.pop(0)
        # translate scene from Chinese to English
        for s in scene_time:
            sceneChinese = s["Scene"]
            sceneEng = sceneChinese2English(sceneChinese)
            s["Scene"] = sceneEng
        
        for tarce in filedict[each]["trace"]:
            # read trace file
            out = logScanf(tarce, fmt, index)
            # add scene tag (default other)
            out.insert(out.shape[1], "scene", "other")
            
            if out is not None:
                # add scene tag
                trace_time = out["time"]
                #for every scene in jsonfile
                for s in scene_time:
                    bottom = int(s["BeginTime"])
                    top = int(s["EndTime"])
                    scene_time_slice, trace_time_scene_index = sliceTime(trace_time, bottom, top)
                    out.loc[trace_time_scene_index,"scene"] = s["Scene"]
                out.to_csv(os.path.join(save_path, "data{}.csv".format(count)))
                count += 1
        
        # end
