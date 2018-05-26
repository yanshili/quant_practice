
import tushare as ts
import pymysql as mdb
import datetime

# Obtain a database connection to the MySQL instance
db_host = 'localhost'
db_user = 'root'
db_pass = '468035416'
db_name = 'securities_master'
con = mdb.connect(db_host, db_user, db_pass, db_name, charset="utf8")


if __name__ == "__main__":

    now = datetime.datetime.utcnow()
    hs300 = ts.get_hs300s()
    symbols = []
    for i in range(len(hs300[0:]['code'])):
        symbols.append(
            (
                str(hs300[0:]['code'][i]), str(hs300[0:]['name'][i]), float(hs300[0:]['weight'][i]), now, now
            )
        )
    print(symbols)
    column_str = """
                 code, name, weight, created_date, last_updated_date
                 """
    insert_str = ("%s, " * 5)[:-2]
    final_str = "INSERT INTO symbol_hs300 (%s) VALUES (%s)" % \
                (column_str, insert_str)
    with con:
        cur = con.cursor()
        cur.executemany(final_str, symbols)

