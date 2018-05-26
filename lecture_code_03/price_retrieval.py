#!/usr/bin/python
# -*- coding: utf-8 -*-

# price_retrieval.py

from __future__ import print_function

import datetime
import time
import csv
import re

import pymysql as mdb
import requests


# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'root'
db_pass = '468035416'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name)


def obtain_list_of_db_tickers():
    """
    Obtains a list of the ticker symbols in the database.
    """
    with con:
        cur = con.cursor()
        cur.execute("SELECT id, ticker FROM symbol")
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]


def get_daily_historic_raw_data_yahoo(ticker
                                      , start_date=time.mktime(time.strptime('2000-01-01', '%Y-%m-%d'))
                                      , end_date=time.time()
                                      , crumb="M80VGzS8nt0"):
    ticker_tup = (
        ticker, int(start_date), int(end_date), '1d', crumb
    )
    yahoo_url = "https://query1.finance.yahoo.com/v7/finance/download/"
    yahoo_url += "%s?period1=%s&period2=%s&interval=%s&events=history&crumb=%s"
    yahoo_url = yahoo_url % ticker_tup
    print("=================================获取prices开始=============================================")
    print(yahoo_url)

    # Try connecting to Yahoo Finance and obtaining the data
    # On failure, print an error message.
    try:
        c_v = "B=5ah7k45dffcs3&b=3&s=8v; ucs=lnct=1526117319; PRF=t%3DMMM%252BBTC-USD%252BCHTR%26fin-trd-cue%3D1; yvapF=%7B%22vl%22%3A39.426407%2C%22rvl%22%3A32.426407%2C%22al%22%3A45.525526%2C%22rcc%22%3A1%2C%22ac%22%3A3%2C%22cc%22%3A1%7D; GUC=AQEBAQFa-NFb3kIdcQRs&s=AQAAAFoADJz7&g=WveFWw; cmp=t=1526181309&j=0"
        headers = {
            "authority": "finance.yahoo.com",
            "method": "GET",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            "cookie": c_v
        }
        print("headers==%s" % headers)
        print('准备获取prices的数据...')
        r = requests.get(yahoo_url, headers=headers)
        print('已获取到获取prices的response')
        # with open("MMM.csv", "wb") as code:
        #     code.write(r.content)
        print('prices数据==%s' % r.text)
    except Exception as e:
        print("Could not download Yahoo data: %s" % e)
    print("=================================获取prices结束=============================================")
    return r.text


def get_daily_historic_data_yahoo(
        ticker, start_date=time.mktime(time.strptime('2000-01-01', '%Y-%m-%d')),
        end_date=time.time(), cookie_v="", crumb="M80VGzS8nt0"
    ):
    """
    Obtains data from Yahoo Finance returns and a list of tuples.

    ticker: Yahoo Finance ticker symbol, e.g. "GOOG" for Google, Inc.
    start_date: Start date in (YYYY, M, D) format
    end_date: End date in (YYYY, M, D) format
    """
    # Construct the Yahoo URL with the correct integer query parameters
    # # for start and end dates. Note that some parameters are zero-based!
    # ticker_tup = (
    #     ticker, start_date[1]-1, start_date[2],
    #     start_date[0], end_date[1]-1, end_date[2],
    #     end_date[0]
    # )
    # yahoo_url = "http://ichart.finance.yahoo.com/table.csv"
    # yahoo_url += "?s=%s&a=%s&b=%s&c=%s&d=%s&e=%s&f=%s"
    ticker_tup = (
        ticker, int(start_date), int(end_date), '1d', crumb
    )
    yahoo_url = "https://query1.finance.yahoo.com/v7/finance/download/"
    yahoo_url += "%s?period1=%s&period2=%s&interval=%s&events=history&crumb=%s"
    yahoo_url = yahoo_url % ticker_tup
    print("=================================获取prices开始=============================================")
    print(yahoo_url)

    # Try connecting to Yahoo Finance and obtaining the data
    # On failure, print an error message.
    try:
        c_v = "B=5ah7k45dffcs3&b=3&s=8v; ucs=lnct=1526117319; PRF=t%3DMMM%252BBTC-USD%252BCHTR%26fin-trd-cue%3D1; yvapF=%7B%22vl%22%3A39.426407%2C%22rvl%22%3A32.426407%2C%22al%22%3A45.525526%2C%22rcc%22%3A1%2C%22ac%22%3A3%2C%22cc%22%3A1%7D; GUC=AQEBAQFa-NFb3kIdcQRs&s=AQAAAFoADJz7&g=WveFWw; cmp=t=1526181309&j=0"
        headers = {
            "authority": "finance.yahoo.com",
            "method": "GET",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            "cookie": c_v
        }
        print("headers==%s" % headers)
        print('准备获取prices的数据...')
        r = requests.get(yahoo_url, headers = headers)
        print('已获取到获取prices的response')
        # with open("MMM.csv", "wb") as code:
        #     code.write(r.content)
        # print('prices数据==%s' % r.text)
        print('解析prices数据开始')
        yf_data = r.text.split("\n")[1:-1]
        print('prices size==%s' % len(yf_data))
        prices = []
        for y in yf_data:
            p = y.strip().split(',')
            v = float(p[1])
            if v > 0:
                prices.append(
                    (datetime.datetime.strptime(p[0], '%Y-%m-%d'),
                     p[1], p[2], p[3], p[4], p[5], p[6])
                )

        print('解析prices数据结束')
    except Exception as e:
        print("Could not download Yahoo data: %s" % e)
    print("=================================获取prices结束=============================================")
    return prices


def get_cookie_crumb(ticker):
    print("=================================获取cookie和crumb开始=============================================")
    yahoo_url = "https://finance.yahoo.com/quote/%s/history?p=%s" % (ticker, ticker)
    print("获取cookie和crumb的地址==%s" % yahoo_url)
    try:
        headers = {
            "authority": "finance.yahoo.com",
            "method": "GET",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X ) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
            # "cookie": "B=7r4ba9hdffb6c&b=3&s=j9"
        }
        print('准备获取cookie和crumb的内容...')
        r = requests.get(yahoo_url, headers = headers)
        print('已获取到获取cookie和crumb的response')

        cookies = r.cookies.get_dict().items()
        print('cookies==%s' % cookies)

        for k, v in cookies:
            if k is "B":
                cookie_v = v

        crumb = re.search('"CrumbStore":{"crumb":".*?"}', r.text, flags=0).group(0).split("\"")[-2]

        print(r.text)
    except Exception as e:
        print("Could not download Yahoo data: %s" % e)
    print("已获取到获取cookie==%s和crumb==%s" % (cookie_v, crumb))
    print("=================================获取cookie和crumb结束=============================================")
    return cookie_v, crumb


def insert_daily_data_into_db(
        data_vendor_id, symbol_id, daily_data
    ):
    """
    Takes a list of tuples of daily data and adds it to the
    MySQL database. Appends the vendor ID and symbol ID to the data.

    daily_data: List of tuples of the OHLC data (with
    adj_close and volume)
    """
    print("=================================保存prices数据到数据库开始=============================================")

    # Create the time now
    now = datetime.datetime.utcnow()

    # Amend the data to include the vendor ID and symbol ID
    daily_data = [
        (data_vendor_id, symbol_id, d[0], now, now,
        d[1], d[2], d[3], d[4], d[5], d[6])
        for d in daily_data
    ]

    # Create the insert strings
    column_str = """data_vendor_id, symbol_id, price_date, created_date, 
                 last_updated_date, open_price, high_price, low_price, 
                 close_price, volume, adj_close_price"""
    insert_str = ("%s, " * 11)[:-2]
    final_str = "INSERT INTO daily_price (%s) VALUES (%s)" % \
        (column_str, insert_str)

    print("daily_data==%s" % daily_data)

    # Using the MySQL connection, carry out an INSERT INTO for every symbol
    with con:
        cur = con.cursor()
        insert_num = cur.executemany(final_str, daily_data)
        print('insert num==%s' % insert_num)
    print("=================================保存prices数据到数据库结束=============================================")


if __name__ == "__main__":
    # This ignores the warnings regarding Data Truncation
    # from the Yahoo precision to Decimal(19,4) datatypes
    # warnings.filterwarnings('ignore')
    #
    # # Loop over the tickers and insert the daily historical
    # # data into the database

    cookie_value = "5ah7k45dffcs3&b=3&s=8v"
    crumb = "M80VGzS8nt0"
    tickers = obtain_list_of_db_tickers()
    lentickers = len(tickers)
    for i, t in enumerate(tickers):
        print(
            "Adding data for %s: %s out of %s" %
            (t[1], i+1, lentickers)
        )
        # if i % 6 == 0:
        #     cookie_value, crumb = get_cookie_crumb(t[1])
        yf_data = get_daily_historic_data_yahoo(t[1], cookie_v=cookie_value, crumb=crumb)
        insert_daily_data_into_db('1', t[0], yf_data)

    print("Successfully added Yahoo Finance pricing data to DB.")

    # yf_data = get_daily_historic_data_yahoo('MMM', cookie_v=cookie_value, crumb=crumb)
    # print(yf_data)
    #
    # cookie, crumb = get_cookie_crumb('MMM')
    # print(cookie, crumb)

    # string = 'alized"}}},"CrumbStore":{"crumb":"WN4sCaYimKs"},"UserStor'
    # match = re.search('"CrumbStore":{"crumb":".*?"}', string, flags=0).group(0).split("\"")[-2]
    # content = match
    # print(content)

    # with con:
    #     cur = con.cursor()
    #     num = cur.execute("select * from daily_price where symbol_id=80;")
    #     print(num)

    # a = None
    # b = "null"
    # if b != "null" and a is not None:
    #     print("b is not null")
    # else:
    #     print("b is null")
