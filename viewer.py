from flask import Flask
app = Flask(__name__)

import MySQLdb

"""
MySQLdb reference: https://mysqlclient.readthedocs.io/index.html
MySQL language: https://dev.mysql.com/doc/refman/8.0/en/
"""

@app.route('/')
def hello_world():
    # Connect to database, retrieve at least the most recent
    # ten items, and display them
    # TODO
    db = MySQLdb.connect(
        user="root", passwd="password", db="sys", host="127.0.0.1", port=3306)
    cur = db.cursor()
    cur.execute("""SELECT * FROM sys.table1 LIMIT 10""")
    data = cur.fetchall()
    print("Latest 10 items")
    for item in data:
        print(item)