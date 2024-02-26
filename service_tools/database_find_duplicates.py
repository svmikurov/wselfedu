"""
Find duplicate values in a SQL table.

Run:
    python3 -m database_find_duplicates
"""
import sqlite3

DB_PATH = '../db-wse-dev.sqlite3'


def find_duplicate_values(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute(
        '''
        SELECT user_id,
               word_id,
               COUNT(*)
        FROM english_worduserknowledgerelation
        GROUP BY user_id,
                 word_id
        HAVING COUNT(*) > 1;
        '''
    )
    duplications = cur.fetchall()

    for index, value in enumerate(duplications):
        print(f'{index}) {value}')

    print('finish')


if __name__ == '__main__':
    find_duplicate_values(DB_PATH)
