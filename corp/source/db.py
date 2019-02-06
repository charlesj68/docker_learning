import MySQLdb
from MySQLdb.cursors import DictCursor
from os import environ


if "BEAN_DB" in environ:
    db_host = environ["BEAN_DB"]
else:
    db_host="db"
db_user = "beaner"
db_passwd = "password"
db_name = "DockBeanBiz"

def connect_db():
    return MySQLdb.connect(
        user=db_user,
        passwd=db_passwd,
        db=db_name,
        host=db_host,
        port=3306,
        cursorclass=DictCursor)
