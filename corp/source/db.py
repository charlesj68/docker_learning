"""Encapsulate connection to MySQL database for Corp service."""
import MySQLdb
from MySQLdb.cursors import DictCursor
from os import environ


# If you are running the Corp service outside the Docker container, then you
# can pass in the IP address of the MySQL container in the BEAN_DB environment
# variable.
if "BEAN_DB" in environ:
    DB_HOST = environ["BEAN_DB"]
else:
    # This value is the name of the MySQL container as defined in the Ansible
    # playbook.
    DB_HOST = "mysqldb"

DB_USER = "beaner"
DB_PASSWD = "password"
DB_NAME = "DockBeanBiz"


def connect_db():
    """Create and return MySQLdb connection."""
    return MySQLdb.connect(
        user=DB_USER,
        passwd=DB_PASSWD,
        db=DB_NAME,
        host=DB_HOST,
        port=3306,
        cursorclass=DictCursor)
