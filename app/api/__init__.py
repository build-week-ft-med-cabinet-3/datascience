import pandas as pd
import sqlite3


def create_db():
    df = pd.read_csv('this will be the csv file jeremy and steven are working on')
    conn = sqlite3.connect('add csv here')
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS add table name")
    df.to_sql("table name", con=conn)


if __name__ == '__main__':
    create_db()
