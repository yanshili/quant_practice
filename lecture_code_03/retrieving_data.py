#!/usr/bin/python
# -*- coding: utf-8 -*-

# retrieving_data.py

from __future__ import print_function

import datetime
import pandas as pd
import pymysql as mdb


def retrieve_daily_price(ticker='', columns=None, oder_column='price_date', index_col='price_date', start=None, end=None):
    # Connect to the MySQL instance
    db_host = 'localhost'
    db_user = 'root'
    db_pass = '468035416'
    db_name = 'securities_master'
    con = mdb.connect(db_host, db_user, db_pass, db_name)
    # Select all of the historic Google adjusted close data
    sql = """SELECT %s
                FROM symbol AS sym
                INNER JOIN daily_price AS dp
                ON dp.symbol_id = sym.id
                WHERE %s
                ORDER BY dp.%s ASC;"""

    if start is not None and end is not None:
        time_sql = "and dp.price_date between '%s' and '%s'" % (start, end)
    else:
        time_sql = ''

    where_sql = "sym.ticker = '%s' %s" % (ticker, time_sql)
    print(where_sql)

    if columns is not None:
        columns_str = (("dp.%s, " * (len(columns) - 1)) + "dp.%s") % columns
    else:
        columns_str = '*'

    final_sql = sql % (columns_str, where_sql, oder_column)

    print(final_sql)
    # Create a pandas dataframe from the SQL query
    goog = pd.read_sql_query(final_sql, con=con, index_col=index_col)

    # Output the dataframe tail
    # print(goog)
    return goog


if __name__ == "__main__":
    # # Connect to the MySQL instance
    # db_host = 'localhost'
    # db_user = 'root'
    # db_pass = '468035416'
    # db_name = 'securities_master'
    # con = mdb.connect(db_host, db_user, db_pass, db_name)
    #
    # # Select all of the historic Google adjusted close data
    # sql = """SELECT dp.price_date, dp.adj_close_price
    #          FROM symbol AS sym
    #          INNER JOIN daily_price AS dp
    #          ON dp.symbol_id = sym.id
    #          WHERE sym.ticker = 'GOOG'
    #          ORDER BY dp.price_date ASC;"""
    #
    # # Create a pandas dataframe from the SQL query
    # goog = pd.read_sql_query(sql, con=con, index_col='price_date')
    #
    # # Output the dataframe tail
    # print(goog.tail())

    data = retrieve_daily_price('GOOG', columns=('price_date', 'adj_close_price')
                         , start=datetime.datetime(2018, 4, 1)
                         , end=datetime.datetime(2018, 5, 1))
    print(data)

