import utils.jsonConvert
import utils.logScanf as logScanf
import GUI.logTimeLine as logTimeLine
import plot.animation.trajectory_animation as trajectory_animation
import decode.decodeTrace as decodeTrace
import os
import utils

def test():

    get =logTimeLine.getFpathandFmt()
    get.mainloop()
    if os.path.exists("timeLineGUI.json"):
        json = utils.jsonConvert.read_json_to_dict("timeLineGUI.json")

    json = get.filepath
    # fmt = r"ins vel xyz:%f, %f, %f"
    # fmt = r"LS-XYZ:%f,%f,%f VEL:%f,%f,%f"
    fmt = r"[T Debug] time:%f,cycleSlipratio:%f,average CN0:%f,average Elevation:%f,vis satellite number:%f,hDop:%f,pDop:%f,ValidLNum:%f, aveEleOfValid:%f"
    # fmt = get.fmt
    columns = get.columns
    columns = ["T", "cSr", "avgCN0", "avgEle", "visSat", "hDop", "pDop", "vLN", "aveEleOfValid"]
    out = logScanf.logScanf(fp, fmt, columns)
    t = logTimeLine.TimeSeriesPlotter(out)
    t.mainloop()
    s  = 1

def testanimation():
    fp = r"D:\DATA\quectelL89HD\L89HD-0103_153617_COM69(EVK).log"
    GNSS, IMU = decodeTrace.readGGAlonandlat(fp)
    l89HDani = trajectory_animation.GNSStraject_INS_animation(GNSS, IMU, None, foretime=100, IMUfreq=100, speed=1,
                                                              save= os.path.join(os.path.dirname(fp), "L89HD250103.mp4"))
    l89HDani.plotinit()
    l89HDani.plot()

    pass
if __name__ == '__main__':
    test()
    testanimation()
    pass