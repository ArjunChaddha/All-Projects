from SupportFile1 import getPoints
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from finta import TA
from matplotlib import style
import matplotlib.dates as mdates
from SupportFile1 import getPoints
from matplotlib.ticker import ScalarFormatter
from mpl_finance import candlestick_ohlc
from matplotlib import ticker
import datetime
from SupportFile2 import StockPlotter, Score
import math

StartDate = '2000-01-01'

class Linear:
    def __init__(self, x1, x2, y1, y2):
        self.m = (y1-y2)/(x1-x2)
        self.c = y1-self.m*x1
        self.x1 = x1
        self.x2 = x2
    def getY(self, x):
        return self.m*x + self.c
    def getM(self):
        return self.m
    def getIndexInRange(self, i):
        return self.x1 <= i <= self.x2
    def addC(self, c):
        self.c += c
    def subtractC(self, c):
        self.c -= c

def getAngle(X0, X1, X2):
    A = np.subtract(X0, X1)
    B = np.subtract(X2, X1)

    magA = np.linalg.norm(A)
    magB = np.linalg.norm(B)

    cosTheta = np.dot(A, B)/(magA*magB)
    theta = math.acos(cosTheta)

    return theta*180/math.pi



def run_(STOCK, RStart, thetaT=20, showPlot_=True):
    data, highs, lows = getPoints(STOCK, R_=RStart, alpha=1, beta=20, combined=False, showPlot=False, getData=True, startDate=StartDate, interval_="1wk")
    data["close"] = np.log10(data["close"])

    linearsHIGH = []
    i = 0
    while i+2 < len(highs):
        x0 = (highs[i])
        X0 = np.asarray([highs[i]/len(data["close"]), data["close"][highs[i]]/max(data["close"]) ])
        done = False
        while not done and i+2<len(highs):
            X1 = np.asarray([highs[i+1]/len(data["close"]), data["close"][highs[i+1]]/max(data["close"]) ])
            X2 = np.asarray([highs[i+2]/len(data["close"]), data["close"][highs[i+2]]/max(data["close"]) ])
            x1 = highs[i+1]
            x2 = highs[i+2]

            theta = getAngle(X0, X1, X2)

            if 180-thetaT <= theta <= 180+thetaT:
                i += 1
                if i+2 == len(highs):
                    lm = Linear(x0, x2, data["close"][x0], data["close"][x2])
                    linearsHIGH.append(lm)
                    i +=1 
                    break
            else:
                done = True
                lm = Linear(x0, x1, data["close"][x0], data["close"][x1])
                linearsHIGH.append(lm)
                # i += 1
        i += 1


    print("\n\n\n, lows\n")
    linearsLOW = []
    i = 0
    while i+2 < len(lows):
        x0 = (lows[i])
        X0 = np.asarray([lows[i]/len(data["close"]), data["close"][lows[i]]/max(data["close"]) ])
        done = False
        while not done and i+2<len(lows):
            X1 = np.asarray([lows[i+1]/len(data["close"]), data["close"][lows[i+1]]/max(data["close"]) ])
            X2 = np.asarray([lows[i+2]/len(data["close"]), data["close"][lows[i+2]]/max(data["close"]) ])
            x1 = lows[i+1]
            x2 = lows[i+2]

            theta = getAngle(X0, X1, X2)

            if 180-thetaT <= theta <= 180+thetaT:
                i += 1
                if i+2 == len(lows):
                    lm = Linear(x0, x2, data["close"][x0], data["close"][x2])
                    linearsLOW.append(lm)
                    i += 1
                    break
            else:
                done = True
                lm = Linear(x0, x1, data["close"][x0], data["close"][x1])
                linearsLOW.append(lm)
                # i += 1
        i += 1

############################################################################
    j = 0
    while j < len(data["close"]):
        y = data["close"][j]
        x = j

        gottenLM = False
        LMselected = None
        selectedLMindex = None
        i = 0
        while not gottenLM and i < len(linearsHIGH):
            lm = linearsHIGH[i]
            if lm.getIndexInRange(x):
                LMselected = lm
                selectedLMindex = i
            i += 1
        if not LMselected == None:
            # print("SUCCESS")
            Yline = LMselected.getY(x)
            dist = Yline - y    
            if dist < 0.001:
                print(i, len(linearsHIGH))
                # linearsHIGH[selectedLMindex].addC(abs(dist))
                # j = -1   
                print(dist)
        else:
            # print("ERROR HERE!!!!", x)
            pass
        j += 1
        

    j = 0
    while j < len(data["close"]):
        y = data["close"][j]
        x = j

        gottenLM = False
        LMselected = None
        selectedLMindex = None
        i = 0
        while not gottenLM and i < len(linearsLOW):
            lm = linearsLOW[i]
            if lm.getIndexInRange(x):
                LMselected = lm
                selectedLMindex = i
            i += 1
        if not LMselected == None:
            Yline = LMselected.getY(x)
            dist = Yline - y    
            if dist > 0.001:
                print(i, len(linearsLOW))
                # linearsLOW[selectedLMindex].subtractC(abs(dist))
                # j = -1   
                print(dist)
        else:
            # print("ERROR HERE!!!!", x)
            pass
        j += 1
###############################################################################
    j = 0
    while j < len(linearsLOW):
        lm = linearsLOW[j]
        xx = np.linspace(lm.x1, lm.x2, 50)
        y = [lm.getY(x) for x in xx]
        plt.plot(xx, y)  
        j += 1
    j = 0
    while j < len(linearsHIGH):
        lm = linearsHIGH[j]
        xx = np.linspace(lm.x1, lm.x2, 50)
        y = [lm.getY(x) for x in xx]
        plt.plot(xx, y)  
        j += 1
    
    if showPlot_:
        plt.plot(np.asarray(data["close"]),'-o', markevery=highs+lows, markersize=5, fillstyle='none')
        # plt.yscale("log")
        plt.show()

    return data, linearsHIGH, linearsLOW, highs, lows



#bntx
if __name__ == "__main__":
    run_("aapl", 1.4, 30)