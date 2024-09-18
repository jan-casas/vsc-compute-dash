import ghhops_server as hs
import psycopg2
from flask import Flask

from src.config.settings import HOST, DB_USER, DB_PASSWORD

# register hops app as middleware
app_hops = Flask(__name__)
hops = hs.Hops(app_hops)


# Define the connection string
@hops.component(
    "/insert_data", name="insert_data", description="insert query for work with postgres databases",
    inputs=[
        hs.HopsString("pg_dbname", "pg_dbname"),
        hs.HopsString("pg_tables", "pg_tables"),
        hs.HopsString("query_sql", "query_sql"),
        hs.HopsBoolean("drop", "drop", default=False),
        hs.HopsBoolean("local", "local", default=True),
        hs.HopsString("online_path", "online_path", default='Null'),
    ],
)
def insert_data(pg_dbname, pg_tables, query_sql, drop, local, online_path) -> None:
    """ Insert query for work with postgres databases

    :param pg_dbname: database name
    :param pg_tables: table name
    :param query_sql: query sql
    :param drop: drop table
    :param local: local database
    :param online_path: online path
    :return: None
    """
    # Use f-strings to make the connection string more readable
    if local:
        conn_string = (f"host={HOST} port=5432 dbname={pg_dbname} user={DB_USER} password="
                       f"{DB_PASSWORD}")
    else:
        with open(online_path, "r") as f:
            lines = f.readlines()
            clean_lines = [l.split("=")[1].split("\n")[0] for l in lines]
            conn_string = (
                f"host={clean_lines[0]} port={clean_lines[1]} dbname={clean_lines[2]} user="
                f"{clean_lines[3]} "
                f"password={clean_lines[4]}")

    with psycopg2.connect(conn_string) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            if drop:
                cursor.execute(f"DROP TABLE IF EXISTS {pg_tables}")
            cursor.execute(query_sql)
        conn.commit()


@hops.component(
    "/get_data", name="get_data", description="Get data from postgres database",
    inputs=[
        hs.HopsString("query_sql", "query_sql"),
        hs.HopsBoolean("local", "local"),
    ],
    outputs=[
        hs.HopsString("values_db", "values_db", "Data from Arduino sensors",
                      hs.HopsParamAccess.LIST),
    ],
)
def get_data(query_sql, local):
    conn_string = conn_string_local if local else conn_string_raspi

    try:
        with psycopg2.connect(conn_string) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(query_sql)
                fetch_data = cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

    values_db = [list(row) for row in fetch_data]

    return values_db


if __name__ == "__main__":
    app_hops.run(debug=False, port=5000)
