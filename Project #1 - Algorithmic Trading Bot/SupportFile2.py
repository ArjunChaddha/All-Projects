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
from SupportFile7 import Job, schedule
import datetime

class obj:
    def __init__(self, i):
        self.elemnet = i
        self.header = i
    def getElement(self):
        return self.elemnet
    def getHeader(self):
        return self.header
    def setHeader(self, h):
        self.header = h


# Class that takes as input the inerval list that was returned above (array conatining inervals
# where the highs are almost the same) When we call getSets on the object, it returns an array
# of sets where each set contanins periods that are overlapping with each other
class Sets:
    # n is length of interval list
    def __init__(self, list_, highs):
        self.list = list_
        self.elements = []
        for i in range(0, len(list_)):
            self.elements.append(obj(i))
    
    def makeSet(self, i, j):
        for e in self.elements:
            if e.getElement() == i:
                i_ = e
            if e.getElement() == j:
                j_ = e
        if i_.getHeader() == j_.getHeader():
            pass
        else:
            hNew = min(i_.getHeader(), j_.getHeader())
            for e in self.elements:
                if e.getHeader() == i_.getHeader() or e.getHeader() == j_.getHeader():
                    e.setHeader(hNew)

    def printout(self):
        for e in self.elements:
            print(e.getElement(), e.getHeader())

    def getSets(self):
        self.setup()

        sets = []
        headers = []
        for e in self.elements:
            if not e.getHeader() in headers:
                headers.append(e.getHeader())
                sets.append([self.list[e.getElement()]])
            else:
                index = headers.index(e.getHeader())
                sets[index].append(self.list[e.getElement()])
        return sets
    
    def setup(self):
        gg = self.getCopatability()
        # print(gg, "iuketjfb")
        for i in gg:
            self.makeSet(i[0], i[1])

    def getCopatability(self):
        intervalList = self.list
        groups = []
        i = 0
        while i < len(intervalList):
            j = i-1
            finish_i = intervalList[i][1]
            start_i = intervalList[i][0]
            
            while j < len(intervalList):
                if not i == j and j>=0:
                    start_j = intervalList[j][0]
                    finish_j = intervalList[j][1]
                    if  start_j < finish_i and finish_j > start_i:
                        groups.append([i, j])
                j += 1
            i += 1
        return groups


class Fibonachi:
    def __init__(self, stock, interval, R, alpha=1, beta=10):
        self.STOCK = stock
        self.INTERVAL = interval
        self.R = R
        self.alpha = alpha
        self.beta = beta
        self.data, self.highs, self.lows = getPoints(self.STOCK, R_=R, alpha=1, beta=20, combined=False, showPlot=False, getData=True, startDate='2000-01-01', interval_=self.INTERVAL)
        # plt.plot(self.data["close"])
        # plt.show()

    def getCoeffsNext(self, highs, start, n):
        # function that takes in as input a list which contains the indexes of the highs(X)
        # it alos takes an input n. The function returns an array. the ith element of that 
        # array is the coeffectent for the linear regression through the ith till i+n turning point            # eg 4th elemnt with n=3 would the the slope of the lin reg with input as 4th to 7th TP 
        # Also X and Y for the lin reg are normalized to that slope stays somehat constat accross stocks
        coeffs = []
        end = start+n
        i = 0
        # print("dszfdxgchvjb", highs)
        while i < len(highs)-n:
            X  = (np.asarray(highs[start+i:i+end])/len(self.data["close"])).reshape(-1, 1)
            
            highPrices = []
            for high in highs[start+i:i+end]:
                highPrices.append(self.data['close'][high])
            Y = (np.asarray(highPrices)/max(highPrices)).reshape(-1, 1)

            if Y.shape[0] > 0:
                reg = LinearRegression()
                reg.fit(X, Y)
                coeff = reg.coef_
                # print(coeff)
                coeffs.append(coeff[0][0])
            i += 1
        # print("jrhwfbda", coeffs)
        return coeffs

    def getIntervalList(self, forward, thresh):
        self.forward = forward
        self.thresh = thresh
        c = self.getCoeffsNext(self.highs, 0, forward)

        pp = []
        for coef in c:
            if abs(coef) <= thresh:
                try:
                    pp.append(c.index(coef))
                except:
                    pass
        
        # print(pp, "4gtvhbejwktgf")
        # if the slope is less than the theshold speciified, then we can assume that there are at least 3 TPS
        # that are more or less the same price. Then we, extend and see if the 4th one also has a slope less
        # than the threshold, is so we check for the 5th point as well. We stop when the slope excends the
        # Threshold and thus get a list on maximas that are more or less the same price so that we can 
        # get the 0,100 levls from those peoriods. At the end we get the array breaklist which has the prooids 
        # where it is more or less constant 
        intervalList = []
        for index in pp:
            # index = pp[0]
            coef = c[index]
            breaks = 0
            broken = False
            i = forward
            while not broken:
                # print("lol is,", i+index)
                X  = (np.asarray(self.highs[index:i+index])/len(self.data["close"])).reshape(-1, 1)
                highPrices = []
                for high in self.highs[index:i+index]:
                    highPrices.append(self.data['close'][high])
                Y = (np.asarray(highPrices)/max(highPrices)).reshape(-1, 1)

                if Y.shape[0] > 0:
                    reg = LinearRegression()
                    reg.fit(X, Y)
                    coeff = reg.coef_
                    pred = reg.predict(X)
                    score = r2_score(Y, pred)
                    # print(index, i+index, coeff, score, "SCORE>>>")
                    if abs(coeff) >= thresh:
                        broken = True
                    else:
                        i += 1
                else:
                    broken = True
                
                if i+index >= len(self.highs):
                    broken = True
                # print(i)
                # print(X)

            # print(index, i+index-1-1)
            intervalList.append([index, i+index-1])


            # print(intervalList)

        # print(intervalList, "edfghjdxgcfgvbjjjgjghjn", forward, thresh)
        return intervalList

    def correctIntervalList(self, intervalList, percentage):
        final = []
        for i in intervalList:
            period = self.highs[i[1]] - self.highs[i[0]]
            total = len(self.data["close"])
            if period/total <= percentage:
                final.append(i)
        return final

    def getStartandEndonHighs(self, sets, start='min', end='min'):
        final = []
        for set_ in sets:
            minStart = min(e[0] for e in set_)
            maxStart = max(e[0] for e in set_)
            minFinish = min(e[1] for e in set_)
            maxFinish = max(e[1] for e in set_)
        
            if start == 'min':
                s_ = minStart
            else:
                s_ = maxStart
            
            if end == 'min':
                f_ = minFinish
            else:
                f_ = maxFinish
            
            final.append([s_, f_])
        return final

    def getStartandEndonClosing(self, sets):
        intervals = self.getStartandEndonHighs(sets)
        ii = []
        for i in intervals:
            if i[1] - i[0] > 2:
                ii.append( [ self.highs[ i[0] ], self.highs[ i[1]-1 ] ] )
        return ii
    
    def getNextLow(self, index):
        i = 0
        while i < len(self.lows):
            if self.lows[i] > index:
                return self.lows[i]
            i += 1
        return None

    def getFinalIntervals(self, forward_, thresh_):
        intervalList = self.correctIntervalList(self.getIntervalList(forward_, thresh_), 0.8)
        s = Sets(intervalList, self.highs)
        finalIntervals = self.getStartandEndonClosing(s.getSets())
        return finalIntervals

    def getFibonachis(self, forward_, thresh_):
        finalIntervals = self.getFinalIntervals(forward_, thresh_)
        fibs = []

        for i in finalIntervals:
            # print(i[0], i[1])

            hundred = max(self.data["close"][i[0]:i[1]])
            # print("Hundred is: ", hundred)
            index = np.where(np.asarray(self.data["close"]) == hundred)
            # print("index is: ", index, data["close"][index[0]])
            zi = self.getNextLow(i[1])
            
            zero = min(self.data["close"][index[0][0]:zi])
            
            # print("zero is: ", zero)
            # print("(100, 0), ", hundred, zero)

            fibs.append([zero, hundred])
        
        return fibs


class StockPlotter:
    def __init__(self, data, highs, lows):
        self.data = data
        self.highs = highs
        self.lows = lows
    
    def plotCandleStick(self, tickerEvery=100):
        data = self.data.copy()

        df_volume = data['volume']

        data = data.reset_index()
        data['Date'] = data['Date'].map(mdates.date2num)
        data = data.drop(['Adj Close', 'volume'], axis=1)
        # print(data.head())


        # fig.tight_layout()
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()
        ax1.set_yscale('log')
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(tickerEvery))  # major y tick positions every 100
        ax1.yaxis.set_minor_locator(ticker.NullLocator())  # no minor ticks
        ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())  # set regular formatting
        ax1.grid(True)

        candlestick_ohlc(ax1, data.values, width=3)

        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

        plt.subplots_adjust(left=0.04, right=0.97, top=0.93, bottom=0.05, wspace=0.2, hspace=0.37)
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()

    def plotCandleStickWithMultipleLevels(self, fibs, tickerEvery=100):
        data = self.data.copy()

        df_volume = data['volume']

        data = data.reset_index()
        data['Date'] = data['Date'].map(mdates.date2num)
        data = data.drop(['Adj Close', 'volume'], axis=1)
        # print(data.head())


        # fig.tight_layout()
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()
        ax1.set_yscale('log')
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(tickerEvery))  # major y tick positions every 100
        ax1.yaxis.set_minor_locator(ticker.NullLocator())  # no minor ticks
        ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())  # set regular formatting
        ax1.grid(True)

        candlestick_ohlc(ax1, data.values, width=3)
        
        k = 0
        cols = ['r', 'k', 'b', 'y', 'm', 'g']
        for f in fibs: 
            try:
                zero = f[0]
                hundred = f[1]
                print(zero, hundred, "______------______------______------______-----")
                zeroIndex = self.data["low"][self.data["low"] == f[0]].index[0]
                hundredIndex = self.data["high"][self.data["high"] == f[1]].index[0]
                print(hundredIndex)
                lastIndex = self.data["high"][self.data["high"] == self.data["high"][-1]].index[0]
                print(zeroIndex, hundredIndex, "ZI, HI")
                zi = self.data["low"].index.get_loc(zeroIndex)
                hi = self.data["high"].index.get_loc(hundredIndex)
                print(hi, "hi")
                if (hi < zi):
                    # ax1.axhline((hi,zero), (len(data["close"]), zero), label=str(round(zero, 2)) + '  ' +str(zeroIndex)[:-8], color = 'r')
                    # ax1.axhline((hi,hundred), (len(data["close"]), hundred), label=str(round(hundred, 2)) + '  ' + str(hundredIndex)[:-8], color = 'r')
                    ax1.plot([hundredIndex,lastIndex], [zero, zero], label=str(round(zero, 2)) + '  ' +str(zeroIndex)[:-8], color = cols[k])
                    ax1.plot([hundredIndex,lastIndex], [hundred, hundred], label=str(round(hundred, 2)) + '  ' + str(hundredIndex)[:-8], color = cols[k])
                    ax1.annotate(str(round(zero, 2)), xy=(hundredIndex, zero), xytext=(hundredIndex, zero+4))
                    ax1.annotate(str(round(hundred, 2)), xy=(hundredIndex, hundred), xytext=(hundredIndex, hundred+4))
                        
                
                    nums = [1.618, 2.618, 4.236, 6.854, 11.09, 17.944]
                    # cols = ['r', 'k', 'b', 'y', 'm', 'g']
                    i = 0
                    for num in nums:
                        ax1.plot([hundredIndex,lastIndex], [zero+ ((hundred-zero)*num), zero+ ((hundred-zero)*num)], '--', color = cols[k])
                        ax1.annotate(str(round(zero+ ((hundred-zero)*num), 2)) + ' (' + str(num) + ')', xy=(hundredIndex, zero+ ((hundred-zero)*num)), xytext=(hundredIndex, zero+ ((hundred-zero)*num)+4))
                        i += 1
            except:
                print("error in", f[0], f[1])
                pass
            k+= 1

        ax1.legend()    
        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

        plt.subplots_adjust(left=0.04, right=0.97, top=0.93, bottom=0.05, wspace=0.2, hspace=0.37)
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()

    def plotCandleStickWithLevels(self, zero, hundred, tickerEvery=100):
        data = self.data.copy()

        df_volume = data['volume']

        data = data.reset_index()
        data['Date'] = data['Date'].map(mdates.date2num)
        data = data.drop(['Adj Close', 'volume'], axis=1)
        # print(data.head())


        # fig.tight_layout()
        ax1 = plt.subplot2grid((6,1), (0,0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((6,1), (5,0), rowspan=1, colspan=1, sharex=ax1)
        ax1.xaxis_date()
        ax1.set_yscale('log')
        ax1.yaxis.set_major_locator(ticker.MultipleLocator(tickerEvery))  # major y tick positions every 100
        ax1.yaxis.set_minor_locator(ticker.NullLocator())  # no minor ticks
        ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())  # set regular formatting
        ax1.grid(True)

        candlestick_ohlc(ax1, data.values, width=3)

        zeroIndex = self.data["low"][self.data["low"] == zero].index[0]
        hundredIndex = self.data["high"][self.data["high"] == hundred].index[0]
        # zeroIndex = datetime.strptime(str(zeroIndex), '%Y-%m-%d')
        # hundredIndex = datetime.strptime(str(hundredIndex), '%Y-%m-%d') 
        ax1.axhline(zero, label=str(round(zero, 2)) + '  ' +str(zeroIndex)[:-8], color = 'r')
        ax1.axhline(hundred, label=str(round(hundred, 2)) + '  ' + str(hundredIndex)[:-8], color = 'k')
        nums = [1.618, 2.618, 4.236, 6.854, 11.09, 17.944]
        cols = ['r', 'g', 'b', 'y', 'm', 'k']
        i = 0
        for num in nums:
            ax1.axhline( zero+ ((hundred-zero)*num), linestyle='--', label=str(round(zero+ ((hundred-zero)*num), 2)) + '  ' +str(num), color = cols[i])
            i += 1
        ax1.legend()

        ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)

        plt.subplots_adjust(left=0.04, right=0.97, top=0.93, bottom=0.05, wspace=0.2, hspace=0.37)
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.show()





class Score:
    def __init__(self, data, highs, lows):
        self.Tps = highs + lows
        self.data = data
        self.highs = highs
        self.lows = lows
        self.nums = [1.618, 2.618, 4.236, 6.854, 11.09, 17.944]

    def getClosestLevel(self, price, levels):
        d = 1000000000000
        l = None
        for level in levels:
            if abs(price-level) < d:
                d = abs(price-level)
                l = level
        return l

    def scoreFib(self, pDifference, alpha=2):
        if not pDifference == 0:
            return (1/max(0.000001, abs(pDifference)))
        else:
            return 0

    def getScore(self, zero, hundred, thresh=5, nums_=None, avg=False):
        try:
            if nums_ == None:
                nums = self.nums
            else:
                nums = nums_
            
            levels = [zero+ ((hundred-zero)*num) for num in nums]
            levels.append(zero)
            levels.append(hundred)
            zeroIndex = self.data["low"][self.data["low"] == zero].index[0]
            zeroIndex = self.data["low"].index.get_loc(zeroIndex)
            # print(zeroIndex)
            c = 0
            score_ = 0
            for tp in self.Tps:
                if tp >= zeroIndex:
                    price = self.data["close"][tp]
                    level = self.getClosestLevel(price, levels)
                    pDifference = (price-level)/price*100
                    if abs(pDifference) <= thresh:
                        score_ += self.scoreFib(pDifference)
                        # print(fib[0], fib[1], "score is:", scoreFib(pDifference), "diff is", pDifference, "for price", price, "compared to", level)
                        c += 1
            # if not c == 0:
            #     print("avs is", score_/c, "total is:", score_, zero, hundred)
            # else:
            #     print("zero", score_)
            
            if avg:
                if c == 0:
                    return None
                else:
                    return score_/c
            else:
                return score_
        except:
            return None

    # fibonachi = Fibonachi('BABA', "1wk", 1.1811, 1, 20)
    # fibs = fibonachi.getFibonachis(3, 0.7)
    # scorer = Score(data, highs, lows)

    # for fib in fibs:
    #     score = scorer.getScore(fib[0], fib[1])
    #     print("score for (", fib[0], fib[1], ") is:", score)

    #     plotter.plotCandleStickWithLevels(fib[0], fib[1])
 


if __name__ == "__main__":
    stock = "MAR"
    Rs = np.linspace(1.05, 1.7, num=25)
    fibsAll = []

    RStart = 1.15
    while True:
        dataSc, highsSc, lowsSc = getPoints(stock, R_=RStart, alpha=1, beta=10, interval_="1wk" ,combined=False, showPlot=False, getData=True, startDate='2000-01-01')
        plt.plot(dataSc["close"],'-o', markevery=highsSc+lowsSc, markersize=5, fillstyle='none')
        plt.yscale('log')
        plt.show()
        x = input("y for fine, m for more Tps, mm for much-more, l for less Tps, ll for lot-less:  ")
        if x == 'y':
            break
        elif x == 'm':
            RStart -= 0.01
        elif x == 'l':
            RStart += 0.01
        elif x == 'mm':
            RStart -= 0.05
        elif x == 'll':
            RStart += 0.05
        else:
            print("error")

    for R in Rs:
        data, highs, lows = getPoints(stock, R_=R, alpha=1, beta=10, interval_="1wk" ,combined=False, showPlot=False, getData=True, startDate='2000-01-01')
        # plt.plot(data["close"],'-o', markevery=highs+lows, markersize=5, fillstyle='none')
        # plt.show()
    

        plotter = StockPlotter(data, highs, lows)
        fibonachi = Fibonachi(stock, "1wk", R)
        scorer = Score(dataSc, highsSc, lowsSc)

        nums = [2, 3, 4, 5, 6, 7, 8]
        threshs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
        for num in nums:
            for thresh in threshs:
                # fibonachi = Fibonachi('BABA', "1wk", 1.1811, 1, 20)
                fibs = fibonachi.getFibonachis(num, thresh)
                # print("WE GOT THIS FOR A RUN", fibs)
                for fib in fibs:
                    score = scorer.getScore(fib[0], fib[1])
                    avsgScore = scorer.getScore(fib[0], fib[1], avg=True)
                    fibsAll.append([fib, score, avsgScore])

    fibsAll_ = []
    [fibsAll_.append(x) for x in fibsAll if x not in fibsAll_ and not x[1] == None] 

    SortedFibsAll = sorted(fibsAll_, key=lambda x: x[1], reverse=True)
    
    fibsdict = {}
    added = []    
    for fib in SortedFibsAll:
        if not fib[0] in added:
            added.append(fib[0])
            fibsdict[int(fib[0][0])+int(fib[0][1])] = [fib[0], fib[1], fib[2]]
            # finalFibs.append(fib)
        else:
            score = fibsdict[int(fib[0][0])+int(fib[0][1])][1]
            if fib[1] > score:
                fibsdict[int(fib[0][0])+int(fib[0][1])] = [fib[0], fib[1], fib[2]]

    finalFibs = []
    for fib, scores in fibsdict.items():
        finalFibs.append([scores])
            
            
    for s in SortedFibsAll:
        print(s)

    print("___________________FINAL_________________________")
    for s in finalFibs:
        print(s)

    print("\n\nHERE IT COMES \n")
    for s_ in finalFibs:
        s = s_[0]
        if s[1] > 1.3 and s[2] > 0.3 and (s[0][1] - s[0][0])/s[0][0] >= 0.2:
            print(s_)
            # plotter.plotCandleStickWithLevels(s[0][0], s[0][1])
    print("\n\nHERE IT FINISHES \n\n\n")

    # for s_ in finalFibs[:3]:
    #     s = s_[0]
    #     if s[1] > 1.3 and s[2] > 0.3 and (s[0][1] - s[0][0])/s[0][0] >= 0.2:
    #         # print(s_)
    #         plotter.plotCandleStickWithLevels(s[0][0], s[0][1])

    jobs = []
    for s_ in finalFibs:
        s = s_[0]
        if s[1] > 1.3 and s[2] > 0.3 and (s[0][1] - s[0][0])/s[0][0] >= 0.2:
            job = Job(s[0][0], s[0][1], s[1])
            jobs.append(job)

    print("\n\n\nHERE IT IS THE FINAL ONES ")
    fibsSelected = schedule(jobs)
    fibsSelected.reverse()
    print("OK THEN \n\n\n\n")

    # plotter.plotCandleStickWithMultipleLevels(fibsSelected)

    for f in fibsSelected:
        plotter.plotCandleStickWithLevels(f[0], f[1])

    data, highs, lows = getPoints(stock, R_=1.15, alpha=1, beta=10, interval_="1wk" ,combined=False, showPlot=False, getData=True, startDate='2000-01-01')    
    plt.plot(data["close"])
    plt.show()
    fig, (ax1, ax2) = plt.subplots(1, 2)
    i = 1
    for s_ in finalFibs:
        s = s_[0]
        range_ = max(data["close"] - min(data["close"]))
        if s[1] > 1.3 and s[2] > 0.3 and (s[0][1] - s[0][0])/s[0][0] >= 0.2 and (s[0][1] - s[0][0])/range_ < 0.5:

            zeroIndex = data["close"][data["close"] == s[0][0]].index[0]
            zeroIndex = data["close"].index.get_loc(zeroIndex)

            hundredIndex = data["close"][data["close"] == s[0][1]].index[0]
            hundredIndex = data["close"].index.get_loc(hundredIndex)

            point1 = [zeroIndex, i]
            point2 = [hundredIndex, i]

            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]

            # fig.suptitle('FIB')

            ax1.plot(x_values, y_values)
            
            point1 = [s[0][0], i]
            point2 = [s[0][1], i]

            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]

            ax2.plot(x_values, y_values)

            i += 1
    ax1.title.set_text('Index')
    ax2.title.set_text('Prices')
    plt.show()
