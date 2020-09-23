import pandas as pd
import sqlite3


def create_db():
    df = pd.read_csv('data/cannabis_final.csv', index_col='strain_id')
    #df = df.set_index('strain_id')
    #df = df.drop('Unnamed: 0', axis=1)
    conn = sqlite3.connect('data/cannabis.sqlite3')
    curs = conn.cursor()
    curs.execute("DROP TABLE IF EXISTS Cannabis")
    df.to_sql("Cannabis", con=conn)


if __name__ == '__main__':
    create_db()
