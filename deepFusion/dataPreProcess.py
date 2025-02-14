'''
Author: Withoutwaxwqy 2137697992@qq.com
Date: 2025-02-10 15:22:56
LastEditors: error: error: git config user.name & please set dead value or install git && error: git config user.email & please set dead value or install git & please set dead value or install git
LastEditTime: 2025-02-13 16:55:27
FilePath: \GNSSutils\deepFusion\dataPreProcess.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from utils.logScanf import logScanf, quectelRootGetTraceAndJson, trace2csv
from utils.jsonConvert import read_json_to_dict

import pandas as pd


# 获取数据

scene = ["openSky", "UnderElevated", "boulevard", "urbanCanyon", "underPass",
         "forest", "garage", "tunnel", "elevated", "multipath", "cityRoad", "highBuilding"]

roots=[r"D:\DATA\quectelDeepScene\LG69T\hefei\GNSS\GNSS\GNSS\10HZ\2023\0614"]


# 读每一个目录下的log文件，还有对应的json
filedict = {}
for root in roots:
    trace, json = quectelRootGetTraceAndJson(root)
    filedict[root] = {"trace": trace, "json": json}

# 保存数据
TDebugfmt = r"[T Debug] time:%f,cycleSlipratio:%f,average CN0:%f,average Elevation:%f,vis satellite number:%f,hDop:%f,pDop:%f,ValidLNum:%f, aveEleOfValid:%f"
index = ["time","cycleSlipratio","average CN0","average Elevation","vis satellite number","hDop","pDop","ValidLNum","aveEleOfValid"]
count = 0
data_save_root = r"D:\private projections\GNSSutils\data\deepLtest\gnssTFtest"


trace2csv(filedict, TDebugfmt, index, data_save_root)
for f in filedict.keys():
    data = logScanf(f, TDebugfmt)
    report_json = read_json_to_dict()


    data.to_csv(os.path.join(data_save_root, "data{}.csv".format(count)))
print("data prepare done! ---------------------------------")



