import re
import pandas as pd
import numpy as np
fix_type= ["No fix", "Fix", "DGPS fix", "PPS fix", "Real Time Kinematic", 
           "Float RTK", "DR", "Manual input mode", "Simulation mode"]

def readGGAlonandlat(file):
    out = []
    counter = 0
    IMUrawData = []
    GGAstart = 0
    with open(file, "rb") as f:
        line = f.readline()
        while line:
            print("\rRead GGA{}".format(counter), end="")
            if line.startswith(b"$PQTMRAWIMU") and GGAstart == 1:
                try:
                    CC = re.split(b",", line[:-5])
                    if len(CC) == 9:
                        IMUrawData.append(list(map(float, CC[1:])))
                    else:
                        print("IMU data error")
                except ValueError:
                    line = f.readline()
                    continue
            if line[3:6] == b"GGA":
                GGAstart = 1
                try:
                    cc = re.split(b",", line)
                    lat = cc[2]
                    lat = float(lat[:2]) + float(lat[2:])/60
                    if cc[3] == b"S":
                        lat = -lat
                    lon = cc[4]
                    lon = float(lon[:3]) + float(lon[3:])/60
                    if cc[5] == b"W":
                        lon = -lon
                    Time = "{:0>2d}:{:0>2d}:{:0>2f}".format(int(cc[1][:2]), int(cc[1][2:4]), float(cc[1][4:]))

                    Quality = fix_type[int(cc[6])]
                    NumSatUsed = int(cc[7])
                    HDOP = float(cc[8])
                    Alt = float(cc[9])
                    Sep= float(cc[11])
                    Show = "Time:{} HDOP:{} Fix type:{}".format(Time, HDOP, Quality)
                    out.append([counter, Time, lon, lat, Quality, NumSatUsed, HDOP, Alt, Sep, Show])
                    counter += 1
                except ValueError:
                    line = f.readline()
                    continue
            elif line.find(b"GGA") != -1:
                GGAstart = 1
                try:
                    cc = re.split(b",")
                    lat = cc[2]
                    lat = float(lat[:2]) + float(lat[2:])/60
                    if cc[3] == b"S":
                        lat = -lat
                    lon = cc[4]
                    lon = float(lon[:3]) + float(lon[3:])/60
                    if cc[5] == b"W":
                        lon = -lon
                    Time = "{:0>2d}:{:0>2d}:{:0>2f}".format(int(cc[1][:2]), int(cc[1][2:4]), float(cc[1][4:]))

                    Quality = fix_type[int(cc[6])]
                    NumSatUsed = int(cc[7])
                    HDOP = float(cc[8])
                    Alt = float(cc[9])
                    Sep= float(cc[11])
                    Show = "Time:{} HDOP:{} Fix type:{}".format(Time, HDOP, Quality)
                    out.append([counter, Time, lon, lat, Quality, NumSatUsed, HDOP, Alt, Sep, Show])
                    counter += 1
                except ValueError:
                    line = f.readline()
                    continue
            line = f.readline()
    dfout = pd.DataFrame(out, columns=["Index", "Time", "Longitude", "Latitude", "Fix type", "NumSatUsed", "HDOP", "Altitude", "Sep", "Show"])
    IMUrawData = pd.DataFrame(np.array(IMUrawData), columns=["Time", "Temp", "GyroX", "GyroY", "GyroZ", "AccX", "AccY", "AccZ"])
    return dfout, IMUrawData