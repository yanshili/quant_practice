#coding:utf-8

import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pprint
import statsmodels.tsa.stattools as ts
from lecture_code_03 import price_retrieval as pr
from hs300 import retrieving_data_hs300 as rd

import pandas_datareader as pdr

import statsmodels.api as sm
#最小二乘
from statsmodels.stats.outliers_influence import summary_table
#获得汇总信息


def plot_price_series(df, ts1, ts2, start, end):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df[ts1], label=ts1)
    ax.plot(df.index, df[ts2], label=ts2)
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start, end)
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('%s and %s Daily Prices' % (ts1, ts2))
    plt.legend()
    plt.show()

def plot_scatter_series(df, ts1, ts2):
    plt.xlabel('%s Price ($)' % ts1)
    plt.ylabel('%s Price ($)' % ts2)
    plt.title('%s and %s Price Scatterplot' % (ts1, ts2))
    plt.scatter(df[ts1], df[ts2])
    plt.show()

def plot_residuals(df, start, end):
    months = mdates.MonthLocator()  # every month
    fig, ax = plt.subplots()
    ax.plot(df.index, df["res"], label="Residuals")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    ax.set_xlim(start, end)
    ax.grid(True)
    fig.autofmt_xdate()

    plt.xlabel('Month/Year')
    plt.ylabel('Price ($)')
    plt.title('Residual Plot')
    plt.legend()

    plt.plot(df["res"])
    plt.show()


def retrieve_ticker_prices(TICKER, start, end):
    ticker_data = rd.retrieve_daily_price(TICKER, columns=('price_date', 'close_price'), start=start, end=end)
    return ticker_data["close_price"]


def calculate_adf(residuals):
    '''
    dtype: float64
    :param residuals:
    :return:
    Results of Dickey-Fuller Test:
    Test Statistic                  -1.536597
    p-value                          0.515336
    #Lags Used                      12.000000
    Number of Observations Used    101.000000
    Critical Value (1%)             -3.496818
    Critical Value (5%)             -2.890611
    Critical Value (10%)            -2.582277
    '''
    # Calculate and output the CADF test on the residuals
    cadf = ts.adfuller(residuals, maxlag=2)
    pprint.pprint(cadf)
    print('\n')
    if cadf[0] > cadf[4].get("5%"):
        print("Test Statistic %s > Critical Value (5percent) %s 是随机游走关系" % (cadf[0], cadf[4].get("5%")))
    else:
        print("Test Statistic %s > Critical Value (55percent) %s 不是随机游走关系" % (cadf[0], cadf[4].get("5%")))
    return cadf


def compare_two_tickers(TICKER_A, TICKER_B):
    start = datetime.datetime(2017, 5, 1)
    end = datetime.datetime(2018, 5, 27)

    df = pd.DataFrame(columns=(TICKER_A, TICKER_B))
    df[TICKER_A] = retrieve_ticker_prices(TICKER_A, start, end)
    df[TICKER_B] = retrieve_ticker_prices(TICKER_B, start, end)
    print(df)

    # Plot the two time series
    plot_price_series(df, TICKER_A, TICKER_B, start, end)

    # Display a scatter plot of the two time series
    plot_scatter_series(df, TICKER_A, TICKER_B)

    # Calculate optimal hedge ratio "beta"
    res = sm.OLS(endog=df[TICKER_B], exog=df[TICKER_A]).fit()
    st, data, ss2 = summary_table(res, alpha=0.05)  # 置信水平alpha=5%，st数据汇总，data数据详情，ss2数据列名

    # beta_hr = data[:2]  # 等价于res.fittedvalues
    beta_hr = res.params[TICKER_A]
    # beta_hr = res.fittedvalues #获取拟合y值
    # res.params  # 拟合回归模型参数
    # res.params[0] + res.params[1] * daily_data['temp'] == res.fittedvalues  # 验证二维回归模型的拟合y值计算原理

    # Calculate the residuals of the linear combination
    df["res"] = df[TICKER_A] - beta_hr * df[TICKER_B]
    print('===============')
    print(beta_hr)
    print('===============')
    print(df['res'])

    # Plot the residuals
    plot_residuals(df, start, end)

    # Calculate and output the CADF test on the residuals
    calculate_adf(df['res'])


if __name__ == "__main__":
    compare_two_tickers("贵州茅台", "五 粮 液")
    # data = retrieve_ticker_prices("AAPL", datetime.datetime(2018, 1, 1), datetime.datetime(2018, 5, 26))
    # data = [1,1.01,1,1,1,1,1,1.1,1,1,1,1,1,1.2,1,1,1,1,1,1,1,1,1,1.1,1,1,1,1,1,1,1.1]
    # calculate_adf(data)
