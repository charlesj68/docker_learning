import MySQLdb
import _mysql_exceptions
from time import (sleep, strftime)

"""
MySQLdb reference: https://mysqlclient.readthedocs.io/index.html
MySQL language: https://dev.mysql.com/doc/refman/8.0/en/
"""
host = "db"
CONNECT_RETRY_TIMEOUT = 10
ORDER_INTERVAL_TIMEOUT = 10

# SQL Statements
SQL_MENU_ITEMS = """
    SELECT menu_item_id, item_name FROM menu;"""

SQL_INSERT_ORDER = """
    INSERT
        INTO `orders` 
            (`menu_item_id`, `quantity`, `placement_time`)
        VALUES
            ({},{},'{}');"""


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

    # Get the list of possible menu items
    # BUG: This list is static! If we add a new menu item while Creator is
    # running then Creator will know nothing of it.
    cur = db.cursor()
    cur.execute(SQL_MENU_ITEMS)
    # Kinda dangerous, except we know the menu is of limited size
    menu = [
        {"menu_item_id": item[0], "item_name": item[1]}
        for item in cur.fetchall()]
    # Perform inserts until we're shut down
    print("Start inserts")
    while (True):
        print("Add an order")
        # RNG menu item
        item = 1
        # RNG quantity
        quantity = 1
        sql = SQL_INSERT_ORDER.format(
            item, quantity, strftime('%Y-%m-%d %H:%M:%S'))
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        sleep(ORDER_INTERVAL_TIMEOUT)
        # Only one cycle for now
        break

    print("Shutdown")

if __name__ == "__main__":
    main()
