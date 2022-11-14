import psycopg2

from luigi_demo.common import config


def get_connection():
    return psycopg2.connect(
        host=config["DB_HOST"],
        port=int(config["DB_PORT"]),
        database=config["DB_NAME"],
        user=config["DB_USER"],
        password=config["DB_PASSWORD"]
    )


def get_cursor(connection):
    return connection.cursor()
