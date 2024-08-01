from matplotlib import pyplot as plt
import numpy as np
from tabulate import tabulate
import requests
import json
import traceback
import time
import sys

class Plotter():
    def __init__(self, figsize = None, dev = (1,1)):
        self.fig = plt.figure(figsize=figsize, tight_layout=True)
        self.ax = self.fig.add_subplot()
        self.cmap = plt.get_cmap("tab10")
        self.dev = dev

    def plot2d(self, x, y, pos=1 ,xlim=[], ylim=[], label="", label_loc="best", xlabel="", ylabel="", title="", file_name="", x_log=False, y_log=False, grid=False, color=False, ls=False):
        if not pos > (self.dev[0]*self.dev[1]):        
            self.ax = self.fig.add_subplot(self.dev[0], self.dev[1], pos)
        else :
            raise ValueError
        
        if not color:
            color = np.full(len(y), "", dtype=object)
        if not ls:
            ls = np.full(len(y), "", dtype=object)
        
        if y.ndim == 1 and type(y[0]) is not list and type(y[0]) is not np.ndarray:
            if color[0] == "":
                color[0] = "b"

            if ls[0] == "":
                ls[0] = "solid"

            if label == "":
                self.ax.plot(x, y, c=color[0], ls=ls[0])
            else:
                self.ax.plot(x, y, c=color[0], ls=ls[0], label=label)
                self.ax.legend(loc=label_loc)
        else:
            if not ls[0]:
                ls = np.array(["solid"] * len(y))

            if x.ndim == 1 and type(x[0]) is not list and type(x[0]) is not np.ndarray:
                if label == "":
                    for i in range(len(y)):
                        if not color[i]:
                            self.ax.plot(x, y[i], c=self.cmap(i), ls=ls[i])
                        else:
                            self.ax.plot(x, y[i], c=color[i], ls=ls[i])
                else:
                    for i in range(len(y)):
                        if not color[i]:
                            self.ax.plot(x, y[i], c=self.cmap(i), ls=ls[i], label=label[i])
                        else:
                            self.ax.plot(x, y[i], c=color[i], ls=ls[i], label=label[i])
                    self.ax.legend(loc=label_loc)
            else:
                if label == "":
                    for i in range(len(y)):
                        if not color[i]:
                            self.ax.plot(x[i], y[i], c=self.cmap(i), ls=ls[i])
                        else:
                            self.ax.plot(x[i], y[i], c=color[i], ls=ls[i])
                else:
                    for i in range(len(y)):
                        if not color[i]:
                            self.ax.plot(x[i], y[i], c=self.cmap(i), ls=ls[i], label=label[i])
                        else:
                            self.ax.plot(x[i], y[i], c=color[i], ls=ls[i], label=label[i])
                    self.ax.legend(loc=label_loc)
        if x_log:
            self.ax.set_xscale("log")
        if y_log:
            self.ax.set_yscale("log")
        if xlim != []:
            self.ax.set_xlim(xlim[0], xlim[1])
        if ylim != []:
            self.ax.set_ylim(ylim[0],ylim[1])
        # plt.xticks(fontsize=18)
        # plt.yticks(fontsize=18)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_title(title)
        if grid:
            self.ax.grid()
        if file_name != "":
            plt.savefig(f'{file_name}.jpg',bbox_inches='tight')

            

            
def table_print(headers, contents):
    table = tabulate(contents, headers, tablefmt='grid')
    print(table)    
    
##二分法
def bisec(f, a, b, e):
    while abs(f(b)) > e:
        m = (a + b) / 2
        if f(a)*f(m) > 0:
            a = m 
        else:
            b = m 
        if abs(f(a)) < abs(f(b)): # bが最適な値にする
            a, b = b, a
    return b


def post_message(message):
    webhook_url = "https://hooks.slack.com/services/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"
    
    payload = {
        "text": message
    }
    response = requests.post(
        webhook_url, data=json.dumps(payload),
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        print("Slack notification sent successfully")
    else:
        print(f"Failed to send Slack notification: {response.status_code}, {response.text}")
        
        
def send_notification(method, args, file):
    try:
        start = time.time()
        method(*args)
    except Exception as e:
        error_message = traceback.format_exc()
        time_taken = time.time() - start
        print(error_message, file=sys.stderr)
        post_message(f"===\nPythonスクリプトの処理がエラー終了しました。\nError: {error_message}\ntime_taken:{time_taken}s \n===")
        sys.exit(1)
    else:
        post_message(f"===\nPythonスクリプトの処理が完了しました。\nfunction: {method.__name__}\nfileName: {file}\n===")