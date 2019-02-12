"""Provide a stream of random orders to exercise the services."""
import requests
from threading import Thread, active_count
from time import sleep
from numpy.random import (poisson, randint)

# Constants
MAX_ORDERS = 2  # Total number of orders to create
MAX_QUEUE = 3   # Maximum number of parallel orders to allow
LOOP_TIMEOUT = 2    # Time in seconds to wait before new order creation

#CORP_HOST = 'corp'
CORP_HOST = '172.17.0.4'
# LOCATIONS_HOST = 'locations'
LOCATIONS_HOST = '172.17.0.5'

class my_rest_wrapper(object):
    """Encapsulate a REST API."""

    def __init__(self, url, scheme="http", port="80"):
        """Initialize the interface."""
        self.scheme = scheme
        self.root_url = url
        self.port = port

    def build_url(self, endpoint):
        """Build an endpoint URL with host and port."""
        if hasattr(self, "port"):
            return "{}://{}:{}/{}".format(
                self.scheme, self.root_url, self.port, endpoint)
        else:
            return "{}://{}/{}".format(
                self.scheme, self.root_url, endpoint)


class order_service(my_rest_wrapper):
    """Orders API."""

    def __init__(self):
        """Initialize the interface."""
        url = LOCATIONS_HOST
        port = 5000
        my_rest_wrapper.__init__(self, url, port=port)

    def post_order(self, order):
        """POST a new order."""
        url = self.build_url("orders/")
        res = requests.post(url, json=order)
        if res.ok:
            return res.json()
        return None

    def move_status(self, id, new_status):
        """PUT a status update for an order."""
        url = self.build_url("orders/{}/status/{}".format(id, new_status))
        res = requests.put(url)


class corp_service(my_rest_wrapper):
    """Corp API."""

    def __init__(self):
        """Initialize the interface."""
        url = CORP_HOST
        port = 5000
        my_rest_wrapper.__init__(self, url, port=port)

    def get_menu_items(self):
        """Retreive current menu items."""
        url = self.build_url("menus/")
        res = requests.get(url)
        if res.ok:
            return [x["item_name"] for x in res.json()]
        return None


def rand_order_size():
    """
    Generate the order size.

    This represents how many separate menu items are included in the order.
    This value follows a Poisson distribution, greater than zero.
    """
    return poisson(2.0) + 1


def generate_customer_order():
    """
    Create an order with random data.

    An order will be a list of dicts, each dict containing a "name" and
    "quantity" member.
    """
    order_size = rand_order_size()
    corp_serv = corp_service()
    menu = corp_serv.get_menu_items()
    order = []
    for _ in range(order_size):
        choice = menu[randint(0, len(menu))]
        howmany = poisson(1.0) + 1
        order.append({"name": choice, "quantity": howmany})
    return order


def order_gen(id):
    """Generate random orders through the service APIs."""
    print("order_gen({}): Running".format(id))
    order_serv = order_service()
    # State: Party arrives and order is placed
    order = generate_customer_order()
    order_id = order_serv.post_order(order)
    # Order sits in queue until picked up by kitchen (0-60 seconds)
    wait_for_prep = randint(0, 60)
    print("order_gen({}): Prep delay {}".format(id, wait_for_prep))
    sleep(wait_for_prep)
    order_serv.move_status(order_id, "preparing")
    # Time passes while order is prepared, then served (60-120 seconds)
    prep_duration = randint(60, 120)
    print("order_gen({}): Prep duration {}".format(id, prep_duration))
    sleep(prep_duration)
    order_serv.move_status(order_id, "served")
    # Time passes while party dines, then pay and leave (120-240 seconds)
    checkout_delay = randint(120, 240)
    print("order_gen({}): Checkout delay {}".format(id, checkout_delay))
    sleep(checkout_delay)
    order_serv.move_status(order_id, "closed")
    print("order_gen({}): Finished".format(id))


def main(order_count):
    """Create and manage threads to generate the orders."""
    for id in range(MAX_ORDERS):
        if active_count() >= MAX_QUEUE:
            print("..All permitted threads running: waiting")
            sleep(LOOP_TIMEOUT)
            print("..Finished waiting")
        o = Thread(target=order_gen, kwargs={"id": id})
        o.start()


if __name__ == "__main__":
    main(MAX_ORDERS)
