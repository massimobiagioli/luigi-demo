import psycopg2


def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="weather-data",
        user="weather-data",
        password="weather-data"
    )


def get_cursor(connection):
    return connection.cursor()
