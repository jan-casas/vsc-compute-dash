import logging
import os

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from config.settings import DDBB_INFO


def execute_sql_file(filename):
    conn, cursor = None, None

    try:
        conn = psycopg2.connect(**DDBB_INFO)

        with open(filename, 'r') as file:
            sql = file.read()

        with conn.cursor() as cursor:
            cursor.execute(sql)
            conn.commit()

    except Exception as e:
        logging.error(f"Error executing SQL file: {e}")

    finally:
        conn.close()
        cursor.close()


def initial_data_load_from_excel(data_folder):
    # Loop through each Excel file in the folder
    for excel_file in os.listdir(data_folder):
        if excel_file.endswith('.xlsx') or excel_file.endswith('.xls'):
            try:
                table_name = os.path.splitext(excel_file)[0]
                file_path = os.path.join(data_folder, excel_file)

                # Read the Excel file
                df = pd.read_excel(file_path)

                # Create a database engine
                engine = create_engine(DDBB_INFO['host'])

                # Insert data into the database
                df.to_sql(table_name, engine, if_exists='append', index=False)

            except Exception as e:
                logging.info(f"Error loading data from {excel_file}: {e}")
                continue
