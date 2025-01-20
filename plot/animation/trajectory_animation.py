"""
trajectory_animation.py

This script generates an animation of GNSS trajectories. It reads GNSS data, processes it, and creates an animated plot to visualize the movement over time.

Functions:
- read_gnss_data(file_path): Reads GNSS data from a specified file.
- process_gnss_data(data): Processes the raw GNSS data for plotting.
- create_animation(processed_data): Creates an animation of the GNSS trajectories.

Usage:
Run this script with the appropriate GNSS data file to generate the trajectory animation.
"""

from matplotlib.animation import FuncAnimation, PillowWriter
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams['animation.ffmpeg_path'] = "D:\\coding\\ffpmeg\\bin\\ffmpeg.exe"



class GNSStraject_INS_animation:
    def __init__(self, sol: pd.DataFrame, IMUraw: pd.DataFrame, extro_indicator:pd.DataFrame, **kwargs):
        self.sol = sol
        self.IMUraw = IMUraw
        self.extro_indicator = extro_indicator
        self.kwargs = kwargs
        if "IMUfreq" in self.kwargs:
            self.IMUfreq = self.kwargs["IMUfreq"]
        else:  
            self.IMUfreq = 100
        if "foretime" in self.kwargs:
            self.foretime = self.kwargs["foretime"]
        else:
            self.foretime = 100
        if "save" in self.kwargs:
            self.save = self.kwargs["save"]
        else:
            self.save = "C:\\Users\\21376\\Videos\\untitle.mp4"

        if "speed" in self.kwargs:
            self.speed = self.kwargs["speed"]
        else:
            self.speed = 1

        if "duration" in self.kwargs:
            self.duration = self.kwargs["duration"]
        else:
            self.duration = None

    def plotinit(self):
        """
        Generates an animation of GNSS trajectories.
        sol: GNSS solution data
        IMUraw: IMU raw data
        extro_indicator: external data indicator
        kwargs: additional arguments for animation customization
        """
        
        
        N = self.sol.shape[0]-1
        

        self.lx = [i for i in np.arange(0, N, self.speed)]
        self.lximu = [i for i in np.arange(0, N*self.IMUfreq, self.speed)]
        if self.duration is not None:
            self.lx = [i for i in np.arange(self.duration[0], self.duration[1], self.speed)]
            self.lximu = [i for i in np.arange(self.duration[0]*self.IMUfreq, self.duration[1]*self.IMUfreq, self.speed)]

        # plot GNSS trajectory
        self.fig = plt.figure(figsize=(12, 8))
        self.ax = self.fig.add_subplot(121, projection='3d')
        self.traj, = self.ax.plot([], [], [], marker="o", linestyle="--", markersize=1, color="red", linewidth=0.5,
                        label="GNSS trajectory")

        # plot IMU data
        self.axG1 = self.fig.add_subplot(4, 4, 7)
        self.lineG1, = self.axG1.plot([], [], linewidth=0.1)
        self.axG1.set_ylim(-5, 5)

        self.axG2 = self.fig.add_subplot(4, 4, 11)
        self.lineG2, = self.axG2.plot([], [], linewidth=0.1)
        self.axG2.set_ylim(-5, 5)

        self.axG3 = self.fig.add_subplot(4, 4, 15)
        self.lineG3, = self.axG3.plot([], [], linewidth=0.1)
        self.axG3.set_ylim(-5, 5)

        self.axA1 = self.fig.add_subplot(4, 4, 8)
        self.lineA1, = self.axA1.plot([], [], linewidth=0.1)
        self.axA1.set_ylim(-1, 1)

        self.axA2 = self.fig.add_subplot(4, 4, 12)
        self.lineA2, = self.axA2.plot([], [], linewidth=0.1)
        self.axA2.set_ylim(-1, 1)

        self.axA3 = self.fig.add_subplot(4, 4, 16)
        self.lineA3, = self.axA3.plot([], [], linewidth=0.1)
        self.axA3.set_ylim(-1, 3)

        # plot MAP
        self.axMAP = self.fig.add_subplot(4, 4, 14)

    
    def animation_init(self):
        self.traj.set_data([], [])
        self.traj.set_3d_properties([])

        self.lineG1.set_data([], [])
        self.axG1.set_ylabel("GyroX")
        self.lineG2.set_data([], [])
        self.axG2.set_ylabel("GyroY")
        self.lineG3.set_data([], [])
        self.axG3.set_ylabel("GyroZ")

        self.lineA1.set_data([], [])
        self.axA1.set_ylabel("AccX")
        self.lineA2.set_data([], [])
        self.axA2.set_ylabel("AccY")
        self.lineA3.set_data([], [])
        self.axA3.set_ylabel("AccZ")

        return self.traj, self.lineG1, self.lineG2, self.lineG3, self.lineA1, self.lineA2, self.lineA3


    def animation_update(self, i):
        """
        Update function for the animation.
        i: frame index
        """
        # --- print progress ---
        print("\rProcessing frame {}/{}".format(i, len(self.lx)), end="\r")
        
        #----------------- update GNSS trajectory --------------------------------
        self.traj.set_data(self.sol["Longitude"][:i], self.sol["Latitude"][:i])
        self.traj.set_3d_properties(self.sol["Altitude"][:i])
        if "Fix type" in self.sol.columns:
            if self.sol["Fix type"][i] == "Fix":
                self.traj.set_color("green")
            if self.sol["Fix type"][i] == "DR":
                self.traj.set_color("#708090")
            else:
                self.traj.set_color("red") 
            self.ax.set_title("Fix type: {}\nTime: {}".format(self.sol["Fix type"][i], self.sol["Time"][i]), fontsize=20)
        else:
            self.ax.set_title("Time: {}".format(self.sol["Time"][i]), fontsize=20)

        self.ax.set_xlim(self.sol["Longitude"][i]-(np.max(self.sol["Longitude"])-np.min(self.sol["Longitude"]))/30,
                         self.sol["Longitude"][i]+(np.max(self.sol["Longitude"])-np.min(self.sol["Longitude"]))/30)
        self.ax.set_ylim(self.sol["Latitude"][i]-(np.max(self.sol["Latitude"])-np.min(self.sol["Latitude"]))/30,
                         self.sol["Latitude"][i]+(np.max(self.sol["Latitude"])-np.min(self.sol["Latitude"]))/30)
        self.ax.set_zlim(min(self.sol["Altitude"])-1, max(self.sol["Altitude"])+1)


        # update IMU data
        fore = self.foretime
        Ifq = self.IMUfreq
        if 0< i < fore:
            self.lineG1.set_data(self.lximu[:i*Ifq], self.IMUraw["GyroX"][:i*Ifq])
            self.lineG2.set_data(self.lximu[:i*Ifq], self.IMUraw["GyroY"][:i*Ifq])
            self.lineG3.set_data(self.lximu[:i*Ifq], self.IMUraw["GyroZ"][:i*Ifq])

            self.lineA1.set_data(self.lximu[:i*Ifq], self.IMUraw["AccX"][:i*Ifq])
            self.lineA2.set_data(self.lximu[:i*Ifq], self.IMUraw["AccY"][:i*Ifq])
            self.lineA3.set_data(self.lximu[:i*Ifq], self.IMUraw["AccZ"][:i*Ifq])

            self.axG1.set_xlim(0, self.foretime*Ifq)
            self.axG2.set_xlim(0, self.foretime*Ifq)
            self.axG3.set_xlim(0, self.foretime*Ifq)
            self.axA1.set_xlim(0, self.foretime*Ifq)
            self.axA2.set_xlim(0, self.foretime*Ifq)
            self.axA3.set_xlim(0, self.foretime*Ifq)


        elif i >= fore:
            self.lineG1.set_data(self.lximu[i*Ifq-fore*Ifq:i*Ifq], self.IMUraw["GyroX"][i*Ifq-fore*Ifq:i*Ifq])
            self.lineG2.set_data(self.lximu[i*Ifq-fore*Ifq:i*Ifq], self.IMUraw["GyroY"][i*Ifq-fore*Ifq:i*Ifq])
            self.lineG3.set_data(self.lximu[i*Ifq-fore*Ifq:i*Ifq], self.IMUraw["GyroZ"][i*Ifq-fore*Ifq:i*Ifq])
            self.lineA1.set_data(self.lximu[i*Ifq-fore*Ifq:i*Ifq], self.IMUraw["AccX"][i*Ifq-fore*Ifq:i*Ifq])
            self.lineA2.set_data(self.lximu[i*Ifq-fore*Ifq:i*Ifq], self.IMUraw["AccY"][i*Ifq-fore*Ifq:i*Ifq])
            self.lineA3.set_data(self.lximu[i*Ifq-fore*Ifq:i*Ifq], self.IMUraw["AccZ"][i*Ifq-fore*Ifq:i*Ifq])

            self.axG1.set_xlim((i-self.foretime)*Ifq, i*Ifq)
            self.axG2.set_xlim((i-self.foretime)*Ifq, i*Ifq)
            self.axG3.set_xlim((i-self.foretime)*Ifq, i*Ifq)
            self.axA1.set_xlim((i-self.foretime)*Ifq, i*Ifq)
            self.axA2.set_xlim((i-self.foretime)*Ifq, i*Ifq)
            self.axA3.set_xlim((i-self.foretime)*Ifq, i*Ifq)

        # update MAP
        # self.axMAP.clear()
        # self.axMAP.imshow(self.extro_indicator["Map"][i], cmap="gray")

        return self.traj, self.lineG1, self.lineG2, self.lineG3, self.lineA1, self.lineA2, self.lineA3

    def plot(self):
        ani = FuncAnimation(self.fig, self.animation_update, frames=self.lx, init_func=self.animation_init, blit=True)
        
        # mp4格式
        Writer = animation.FFMpegWriter(fps=16, metadata=dict(artist='Me'))
        ani.save(self.save, writer=Writer)
        plt.show()