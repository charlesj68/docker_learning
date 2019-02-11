from pymongo import MongoClient

def get_order_db():
    client = MongoClient(
        'mongo',
        username='root',
        password='example')
    return client.order_db