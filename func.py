# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 20:15:06 2020

@author: Administrator
"""

import pandas as pd
import numpy as np
from queue import Queue
from scipy import interpolate
import statsmodels.formula.api as smf
import math
import logging
import threading
import re

EXIT = False   # 线程退出信号

class Quantile_Granger():
    """
    创建分位数Granger因果检验类
    """

    def set_range(self, start, end, num):
        '''
        生成估计区间

        Parameters
        ----------
        start : 区间起点
        end : 区间终点
        num : 个数

        Returns
        -------
        qrange : 估计区间列表
        qr_name : 构建区间名

        '''
        qrange = np.linspace(start, end, num)
        T = len(qrange)
        qr_name = [f'[{qrange[i]:.2f}-{qrange[i+1]:.2f}]' for i in range(T-1)]
        return qrange, qr_name

    def pattern(self, df, sign):
        '''
        得到待估计数据字典，受pattern模式影响

        Parameters
        ----------
        df : 原始数据
        sign : 模式选择，包括1,2,3

        Returns
        -------
        DataList : 待估计数据字典
        '''
        DataList = {}
        if sign == '单因素对各市场':
            X = df.iloc[:, 0]
            Xname = df.columns[0]
            for i in range(1, df.shape[1]):
                Y = df.iloc[:, i]
                Yname = df.columns[i]
                DataList[f'{Xname}——>{Yname}'] = pd.DataFrame([X, Y]).T
        elif sign == '相互影响':
            for i in range(df.shape[1]):
                for j in range(df.shape[1]):
                    if i != j:
                        X = df.iloc[:, i]
                        Xname = df.columns.values[i]
                        Y = df.iloc[:, j]
                        Yname = df.columns.values[j]
                        DataList[f'{Xname}——>{Yname}'] = pd.DataFrame([X, Y]).T
        elif sign == '多因素对单市场':
            Y = df.iloc[:, df.shape[1]-1]
            Yname = df.columns.values[df.shape[1]-1]
            for i in range(df.shape[1]-1):
                X = df.iloc[:, i]
                Xname = df.columns.values[i]
                DataList[f'{Xname}——>{Yname}'] = pd.DataFrame([X, Y]).T
        return DataList

    def lag_list(self, Y, X, p=1, q=1):
        '''
        构造待估计滞后序列函数

        Parameters
        ----------
        Y : 被估计变量
        X : 估计变量
        p : X滞后阶数,默认为1
        q : Y滞后阶数,默认为1

        Returns
        -------
        data : 滞后序列

        '''
        data = pd.DataFrame()
        T = len(Y)
        data['y'] = list(Y[max(p, q):T])
        for i in range(1, p+1):
            name = f'y_{i}'
            data[name] = list(Y[max(p, q)-i:T-i])
        for i in range(1, q+1):
            name = f'x_{i}'
            data[name] = list(X[max(p, q)-i:T-i])
        return data

    def qreg(self, data, Q):
        '''
        构造待估计模型函数

        Parameters
        ----------
        data : 滞后序列
        Q : 分位点

        Returns
        -------
        res : 模型估计结果

        '''
        for i, value in enumerate(data):
            if i == 0:
                model = f'{value} ~'
            else:
                model += f' + {value}'
        model = model.replace('~ +', '~')
        mod = smf.quantreg(model, data)
        res = mod.fit(q=Q)
        # print(res.summary())
        return res

    def calculate(self, DataList, qrange, qr_name, max_lag, info_type, WaldNum, sign_num, AicNum, objects=[logging.info]):
        """
        循环计算得到sup_wald值

        Parameters
        ----------
        DataList : 待估计数据字典
        qrange : 估计区间列表
        qr_name : 构建区间名
        max_lag : 最大估计阶数
        info_type : 信息准则类型:AIC或者BIC
        WaldNum : 估计wald值个数,默认1000
        sign_num : 有效数字
        AicNum : 滞后阶数估计数
        objects ：输出信息载体，列表形式

        Returns
        -------
        results : 各区间sup_wald值

        """
        global EXIT
        # 日志设定
        if logging.info in objects:
            logging.basicConfig(filename=r'.\运行结果\运行细节.txt', level=logging.INFO,
                                format='%(asctime)s - %(levelname)s - %(message)s')
        for object in objects:
            object('程序开始运行')
        
        results = pd.DataFrame()
        for key in DataList:
            relation = key
            X = DataList[key].iloc[:, 0]
            Y = DataList[key].iloc[:, 1]

            # 构建滞后阶数队列
            LagQueue = Queue()
            Qspaces = []
            for i in range(AicNum):
                Qspaces.append(i*0.9/(AicNum-1)+0.05)
            for Q in Qspaces:
                for p in range(1, max_lag+1):
                    for q in range(1, max_lag+1):
                        LagQueue.put([Q, p, q])

            # 多线程计算信息准则,选取最优滞后阶数
            self.AicDict = {}

            def info_cri():
                while not EXIT:
                    try:
                        Q, p, q = LagQueue.get(block=False)
                    except:
                        break
                    data = self.lag_list(Y, X, p, q)
                    res = self.qreg(data, Q)
                    n = len(Y)-max(p, q)
                    ssr = []
                    for i in res.resid:
                        if i >= 0:
                            ssr.append(Q*i)
                        else:
                            ssr.append((Q-1)*i)
                    SSE = sum(ssr)/n
                    L = math.log(SSE)
                    k = p+q+1
                    if info_type == 'AIC':
                        AIC = L+k/n
                        NAME = 'AIC'
                    else:
                        AIC = L+(math.log(n)*k)/(2*n)
                        NAME = 'BIC'
                    if Q in self.AicDict:
                        self.AicDict[Q].append([p, q, AIC])
                    else:
                        self.AicDict[Q] = [[p, q, AIC]]
                    for object in objects:
                        object(
                            f'正在进行{relation},分位点:{Q:.2f}的{NAME}计算,滞后阶数为[{p},{q}],{NAME}值为{AIC:.2f}')

            threadCrawl = []
            for i in range(10):
                threadObj = threading.Thread(target=info_cri)
                threadObj.start()
                threadCrawl.append(threadObj)
            for single in threadCrawl:
                single.join()
            for object in objects:
                object(f"计算{relation}最优滞后阶数线程退出循环")

            # 选取最优阶数
            if EXIT: 
                for object in objects:
                    object(f"程序已终止运行")
                return 0
            LagDict = {}
            for i in range(len(qr_name)):
                QAICS = []
                for Q in self.AicDict:
                    if qrange[i] <= Q <= qrange[i+1]:
                        for QAIC in self.AicDict[Q]:
                            QAICS.append(QAIC)
                QAICS = sorted(QAICS, key=lambda x: x[2])
                LagDict[qr_name[i]] = QAICS[0]

            # 生成待估计分位点及滞后阶数组合队列
            QregQueue = Queue()
            Qs = []
            for i in range(WaldNum):
                Qs.append(i*0.9/(WaldNum-1)+0.05)
            for i in range(len(qrange)-1):
                for Q in Qs:
                    if qrange[i] <= Q <= qrange[i+1]:
                        QregQueue.put([Q]+LagDict[qr_name[i]]+[i])
            
            # 11.多线程计算wald值
            self.WaldDict = {}

            def wald_text():
                while not EXIT:
                    try:
                        Q, p, q, aic, index = QregQueue.get(block=False)
                    except:
                        break
                    data = self.lag_list(Y, X, p, q)
                    res = self.qreg(data, Q)
                    wald = ''
                    for i, value in enumerate(data):
                        if i > p:
                            wald += f'{value}='
                    wald = wald + '0'
                    wald = str(res.f_test(wald))
                    walds = float(re.findall('array\(\[\[(.*?)\]\]', wald)[0])
                    self.WaldDict[(Q, index)] = [p, q, walds]
                    for object in objects:
                        object(
                            f'正在进行{relation},分位区间:{qr_name[index]},分位点:{Q:.2f}的wald值,滞后阶数为[{p},{q}],wald值为{walds:.2f}')

            threadCrawl = []
            for i in range(10):
                threadObj = threading.Thread(target=wald_text)
                threadObj.start()
                threadCrawl.append(threadObj)
            for single in threadCrawl:
                single.join()
            for object in objects:
                object(f"计算{relation}的wald线程退出循环")

            # 12.计算Sup-Wald值
            if EXIT: 
                for object in objects:
                    object(f"程序已终止运行")
                return 0
            SupDict = {}
            for i in range(len(qrange)-1):
                SUP = []
                for Q in self.WaldDict:
                    if Q[1] == i:
                        SUP.append(self.WaldDict[Q])
                SUP = sorted(SUP, key=lambda x: x[2], reverse=True)
                SupDict[qr_name[i]] = SUP[0]

            # 13.判断Sup-Wald显著性
            Swl = pd.read_excel(r'.\data\Sup_wald_lag.xlsx')
            tao = []
            for i in range(len(qr_name)):
                fenzi = qrange[i+1]*(1-qrange[i])
                fenmu = qrange[i]*(1-qrange[i+1])
                tao.append(fenzi/fenmu)
            x = Swl[0]
            y = Swl.drop(0, axis=1)
            # 插值拟合
            qr_list = []
            wald_list = []
            for i, qr in enumerate(SupDict):
                q = SupDict[qr][1]
                wald = SupDict[qr][2]
                walds = round(wald, sign_num)
                index = [f'{q}.2', f'{q}.1', q]
                f3 = interpolate.interp1d(x, y[index[0]], kind="quadratic")
                f2 = interpolate.interp1d(x, y[index[1]], kind="quadratic")
                f1 = interpolate.interp1d(x, y[index[2]], kind="quadratic")
                # walds = str(wald)[:str(wald).find('.')+sign_num+1]
                if wald >= f3(tao[i]):
                    wald = f'{walds}***\n[{q}]'
                elif wald >= f2(tao[i]):
                    wald = f'{walds}**\n[{q}]'
                elif wald >= f1(tao[i]):
                    wald = f'{walds}*\n[{q}]'
                else:
                    wald = f'{walds}\n[{q}]'
                qr_list.append(qr)
                wald_list.append(wald)
            results[relation] = pd.Series(wald_list, index=qr_list)
        for object in objects:
            object('分位数Granger因果检验计算结束')
        results.to_excel('./运行结果/Granger.xlsx')
        for object in objects:
            object('估计结果已保存在“运行结果/Granger.xlsx”文件内!')
            object('程序运行结束')


if __name__ == "__main__":  # 用于当前窗体测试

    ex = Quantile_Granger()
    df = pd.read_excel(r'.\data\测试数据.xlsx')
    df = df.drop(df.columns[0], axis=1)

    # 设定参数
    start = 0.1   # 区间起点
    end = 0.9   # 区间终点
    num = 17   # 区间个数
    sign = '单因素对各市场'   # 模式选择
    max_lag = 1   # 最大滞后阶数选择，默认为5
    info_type = 'BIC'   # 信息准则选择
    WaldNum = 35   # 估计wald个数，默认1000个
    sign_num = 2   # 有效数字，默认为3
    AicNum = 20   # 估计各区间最优滞后阶数，默认50个

    # 开始计算
    qrange, qr_name = ex.set_range(start, end, num)
    DataList = ex.pattern(df, sign)
    results = ex.calculate(DataList, qrange, qr_name,
                           max_lag, info_type, WaldNum, sign_num, AicNum)
    results.to_excel('./运行结果/Granger.xlsx')
