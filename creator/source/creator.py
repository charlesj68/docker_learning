import MySQLdb
import _mysql_exceptions
from time import sleep

"""
MySQLdb reference: https://mysqlclient.readthedocs.io/index.html
MySQL language: https://dev.mysql.com/doc/refman/8.0/en/
"""
host = "db"
CONNECT_RETRY_TIMEOUT = 10
ORDER_INTERVAL_TIMEOUT = 10

def main():
    print("App setup")
    db_ready = False
    while (not db_ready):
        print("Connect to db")
        try:
            db = MySQLdb.connect(
                user="beaner", passwd="password",
                db="DockBeanBiz", host=host, port=3306)
            db_ready = True
        except _mysql_exceptions.OperationalError:
            print("Can't connect yet")
            sleep(CONNECT_RETRY_TIMEOUT)
        
    # Perform inserts until we're shut down
    print("Start inserts")
    while (True):
        print("Add an order")
        sleep(ORDER_INTERVAL_TIMEOUT)
    print("Shutdown")

if __name__ == "__main__":
    main()
