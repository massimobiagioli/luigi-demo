from typing import List, Dict

from psycopg2.extras import execute_values

from luigi_demo.common.db import get_connection


def store_weather_data(weather_data: List[Dict[str, any]]):
    connection = get_connection()
    cursor = connection.cursor()

    sql = """
            INSERT INTO weather_forecast (
                detection_date,
                detection_hour,
                city,
                province,
                temperature,
                precipitation,
                humidity,
                wind
            ) VALUES %s
        """

    values = [tuple(weather_data_entry.values()) for weather_data_entry in weather_data]
    print(values)

    execute_values(
        cursor,
        sql,
        values
    )

    connection.commit()
    cursor.close()
    connection.close()
