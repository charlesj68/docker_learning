from flask import Flask
app = Flask(__name__)

import MySQLdb

"""
MySQLdb reference: https://mysqlclient.readthedocs.io/index.html
MySQL language: https://dev.mysql.com/doc/refman/8.0/en/
"""

#host="192.168.1.95"
#host="127.0.0.1"
host="db"
version="1.3"

@app.route('/')
def hello_world():
    # Connect to database, retrieve at least the most recent
    # ten items, and display them
    # TODO
    retval = ""
    db = MySQLdb.connect(
        user="beaner", passwd="password", db="DockBeanBiz", host=host, port=3306)
    cur = db.cursor()
    cur.execute("""SELECT * FROM menu LIMIT 10""")
    data = cur.fetchall()
    retval = "Version {}<br/>".format(version)
    retval += "First 10 menu items<br/>"
    for item in data:
        retval += "{}<br/>".format(item)
    return retval