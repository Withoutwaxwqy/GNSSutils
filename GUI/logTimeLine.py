import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

class getFpathandFmt(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Input File Path and Format")
        self.geometry("700x110")

        # 初始化变量
        self.filepath = ""
        self.fmt = ""
        self.columns = []

        # 创建标签和文本框
        tk.Label(self, text="File Path:", font=("Times", 12)).place(x=20, y=20)
        self.filepath_entry = tk.Entry(self, width=60)
        self.filepath_entry.place(x=150, y=20)

        tk.Label(self, text="Scanf Format:", font=("Times", 12)).place(x=20, y=50)
        self.fmt_entry = tk.Entry(self, width=60)
        self.fmt_entry.place(x=150, y=50)

        tk.Label(self, text="columns name", font=("Times", 12)).place(x=20, y=80)
        self.columns_entry = tk.Entry(self, width=60)
        self.columns_entry.place(x=150, y=80)

        # 创建OK按钮
        ok_button = tk.Button(self, text="OK", command=self.save_and_close)
        ok_button.place(x=670, y=50)

    def save_and_close(self):
        self.filepath = self.filepath_entry.get()
        self.fmt = self.fmt_entry.get()
        temp = re.split("[. ]", self.columns_entry.get())
        self.columns = [t.strip() for t in temp if t.strip()!=""]
        self.destroy()


class TimeSeriesPlotter(tk.Tk):
    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        self.title("Time Series Plotter")
        self.geometry("800x600")

        # 默认标签
        self.label = list(dataframe.columns)[0]
        self.ylim_locked = False
        self.ylim = [0, 0]
        self.num = 20

        # 创建绘图区域
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # 创建下拉菜单
        self.label_var = tk.StringVar(value=self.label)
        label_selector = ttk.Combobox(self, textvariable=self.label_var, values=list(self.dataframe.columns), font=("Times", 20))
        label_selector.pack(pady=5)
        label_selector.bind("<<ComboboxSelected>>", self.change_label)

        # 创建进度条
        self.slider = ttk.Scale(self, from_=0, to=len(self.dataframe)-10, orient="horizontal", command=self.update_plot)
        self.slider.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # 创建文本框
        # 创建文本框
        Label1 = tk.Label(self, text="Enter y-axis limits", font=("Times", 20))
        Label1.pack(side=tk.LEFT)
        self.ylim_entry = tk.Entry(self, text="Enter y-axis limits")
        # self.ylim_entry.place(x=20, y=40)
        self.ylim_entry.pack(side=tk.LEFT)
        self.ylim_entry.bind("<Return>", self.set_ylim)

        # 创建文本框
        # tk.Label(self, text="Enter show number", font=("Times", 20)).place(x=10, y=70)
        # self.shownum = tk.Entry(self, text="Enter show number")
        # self.shownum.place(x=20, y=100)
        # # self.shownum.pack(pady=5)
        # self.shownum.bind("<Return>", self.set_shownum)
        Label2 = tk.Label(self, text="Enter show number", font=("Times", 20))
        Label2.pack(side=tk.LEFT)
        self.shownum = tk.Entry(self, text="Enter show number")
        # self.shownum.place(x=20, y=100)
        self.shownum.pack(side=tk.LEFT)
        self.shownum.bind("<Return>", self.set_shownum)

        # 初始绘图
        self.update_plot(0)


    def change_label(self, event):
        self.label = self.label_var.get()
        self.ylim_locked = False  # 解锁ylim
        self.ylim_entry.delete(0, tk.END)  # 清空文本框
        self.update_plot(self.slider.get())

    def update_plot(self, val):
        start = int(float(val))
        end = start + self.num
        self.ax.clear()
        self.ax.plot(self.dataframe[self.label][start:end])
        self.ax.set_title(f"Data from {start} to {end}", fontsize=16)
        self.ax.set_xlabel("Index", fontsize=16)
        self.ax.set_ylabel(self.label, fontsize=16)
        if self.ylim_locked:
            self.ax.set_ylim(self.ylim[0], self.ylim[1])
        self.canvas.draw()

    def set_ylim(self, event):
        try:
            limits = self.ylim_entry.get().split()
            self.ylim[0], self.ylim[1] = float(limits[0]), float(limits[1])
            self.ax.set_ylim(self.ylim[0], self.ylim[1])
            self.ylim_locked = True  # 锁定ylim
            self.canvas.draw()
        except Exception as e:
            print(f"Error setting y-axis limits: {e}")


    def set_shownum(self, event):
        try:
            limits = self.shownum.get().split()
            self.num = int(limits[0])
            self.canvas.draw()
            self.update_plot(self.slider.get())
        except Exception as e:
            print(f"Error setting show number: {e}")

# 创建并运行GUI
if __name__ == "__main__":
    data = {
    'A': [1, 2, 1, 2, 3, 6, 7, 8, 9, 10, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'B': [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
    'C': [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    }
    df = pd.DataFrame(data)
    app = TimeSeriesPlotter(df)
    app.mainloop()