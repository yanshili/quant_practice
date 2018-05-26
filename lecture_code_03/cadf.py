import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import pprint
import statsmodels.tsa.stattools as ts
from lecture_code_03 import price_retrieval as pr
from lecture_code_03 import retrieving_data as rd

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


if __name__ == "__main__":
    start = datetime.datetime(2010, 4, 1)
    end = datetime.datetime(2018, 5, 1)

    TICKER_A = "AMZN"
    TICKER_B = "AAPL"

    arex = rd.retrieve_daily_price(TICKER_A, columns=('price_date', 'adj_close_price'), start=start, end=end)
    wll = rd.retrieve_daily_price(TICKER_B, columns=('price_date', 'adj_close_price'), start=start, end=end)

    df = pd.DataFrame(columns=(TICKER_A, TICKER_B))
    df[TICKER_A] = arex["adj_close_price"]
    df[TICKER_B] = wll["adj_close_price"]
    print(df)

    # Plot the two time series
    plot_price_series(df, TICKER_A, TICKER_B, start, end)

    # Display a scatter plot of the two time series
    plot_scatter_series(df, TICKER_A, TICKER_B)

    # Calculate optimal hedge ratio "beta"
    res = sm.OLS(endog=df[TICKER_B], exog=df[TICKER_A]).fit()
    st, data, ss2 = summary_table(res, alpha=0.05)   # 置信水平alpha=5%，st数据汇总，data数据详情，ss2数据列名

    beta_hr = data[:, 2]  # 等价于res.fittedvalues
    # beta_hr = res.fittedvalues

    # Calculate the residuals of the linear combination
    df["res"] = df[TICKER_A] - beta_hr*df[TICKER_A]

    # Plot the residuals
    plot_residuals(df, start, end)

    # Calculate and output the CADF test on the residuals
    cadf = ts.adfuller(df["res"])
    pprint.pprint(cadf)
    print('\n')
    if cadf[0] > cadf[4].get("5%"):
        print("因为%s > %s 所以 %s 与 %s 价格是随机游走关系" % (cadf[0], cadf[4].get("5%"), TICKER_A, TICKER_B))
    else:
        print("因为%s < %s 所以 %s 与 %s 价格不是随机游走关系" % (cadf[0], cadf[4].get("5%"), TICKER_A, TICKER_B))
