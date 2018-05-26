
import tushare as ts
import pymysql as mdb
import datetime


# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'root'
db_pass = '468035416'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name, charset="utf8")


def obtain_hs300_stock_codes():
    with con:
        cur = con.cursor()
        cur.execute("select id, code from symbol_hs300")
        data = cur.fetchall()
        return [(d[0], d[1]) for d in data]


def get_stock_daily_prices(code):
    data_frame = ts.get_k_data(code=code, start='2000-01-01', ktype='D', autype='qfq', pause=1)
    prices = []
    for i, d in data_frame.iterrows():
        prices.append(
            (d["date"], d["open"], d["high"], d["low"], d["close"], int(d["volume"]))
        )
    return prices


def insert_daily_data_into_db(data_vendor_id, symbol_code, daily_data):
    now = datetime.datetime.utcnow()

    # Create the insert strings
    column_str = """data_vendor_id, symbol_code, price_date, created_date, 
                    last_updated_date, open_price, high_price, low_price, 
                    close_price, volume"""
    insert_str = ("%s, " * 10)[:-2]
    final_str = "INSERT INTO daily_price_hs300 (%s) VALUES (%s)" % \
                (column_str, insert_str)
    daily_data = [
        (int(data_vendor_id), symbol_code, datetime.datetime.strptime(d[0], '%Y-%m-%d'), now, now,
         d[1], d[2], d[3], d[4], int(d[5]))
        for d in daily_data
    ]
    print(final_str)
    print(daily_data)

    with con:
        cur = con.cursor()
        insert_num = cur.executemany(final_str, daily_data)
        print('insert num==%s' % insert_num)


if __name__ == "__main__":
    stocks = obtain_hs300_stock_codes()

    lenstocks = len(stocks)
    for i, t in enumerate(stocks):
        print(
            "Adding data for %s: %s out of %s" %
            (t[1], i + 1, lenstocks)
        )

        stock_data = get_stock_daily_prices(t[1])
        print(t[1], stock_data)
        insert_daily_data_into_db('1', t[1], stock_data)

    print("Successfully added hs300 stock pricing data to DB.")

    # stock_data = get_stock_daily_prices('600000')
    # print(stock_data)


