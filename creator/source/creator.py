import signal
import sys
from time import (sleep, strftime)
import MySQLdb
import _mysql_exceptions
from numpy.random import (normal, randint)

"""
MySQLdb reference: https://mysqlclient.readthedocs.io/index.html
MySQL language: https://dev.mysql.com/doc/refman/8.0/en/
"""
CONNECT_RETRY_TIMEOUT = 10

# SQL Statements
SQL_MENU_ITEMS = """
    SELECT menu_item_id, item_name FROM menu;"""

SQL_INSERT_ORDER = """
    INSERT
        INTO `orders` 
            (`menu_item_id`, `quantity`, `placement_time`)
        VALUES
            ({},{},'{}');"""

# Global signal to initiate shutdown
shutdown_requested = False

def sigterm_handler(signal, frame):
    shutdown_requested = True


def gen_order_timeout():
    ORDER_INTERVAL_TIMEOUT_MEAN = 10.0
    ORDER_INTERVAL_TIMEOUT_SD = 5.0

    while True:
        timeout = int(normal(
            ORDER_INTERVAL_TIMEOUT_MEAN, ORDER_INTERVAL_TIMEOUT_MEAN, None))
        if timeout > 0:
            break
    print("Generated timeout: {}".format(timeout))
    return timeout


def main():
    global shutdown_requested

    print("App setup")
    db_ready = False
    timeout_limit = 2
    while (not db_ready):
        print("Connect to db")
        try:
            db = MySQLdb.connect(
                user="beaner", passwd="password",
                db="DockBeanBiz", host="db", port=3306)
            db_ready = True
        except _mysql_exceptions.OperationalError:
            print("Can't connect yet")
            sleep(CONNECT_RETRY_TIMEOUT)
        timeout_limit -= 1
        if (timeout_limit < 1):
            exit("Failed to connect to database")

    # Get the list of possible menu items
    # BUG: This list is static! If we add a new menu item while Creator is
    # running then Creator will know nothing of it.
    cur = db.cursor()
    cur.execute(SQL_MENU_ITEMS)
    # Kinda dangerous, except we know the menu is of limited size
    menu = [
        {"menu_item_id": item[0], "item_name": item[1]}
        for item in cur.fetchall()]
    # Now that we're ready to start inserting data, register our term signal
    # handler to close our loop and shutdown
    signal.signal(signal.SIGTERM, sigterm_handler)

    # Perform inserts until we're shut down
    print("Start inserts")
    while (not shutdown_requested):
        print("Add an order")
        item = menu[randint(0, len(menu))]
        quantity = randint(1, 4)
        print("Create order for {} of {}".format(quantity, item["item_name"]))
        sql = SQL_INSERT_ORDER.format(
            item["menu_item_id"], quantity, strftime('%Y-%m-%d %H:%M:%S'))
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        sleep(gen_order_timeout())

    print("Shutdown")
    exit()

if __name__ == "__main__":
    main()
