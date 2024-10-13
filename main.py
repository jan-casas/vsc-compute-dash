from config.settings import PATH_DB_MODEL, PATH_DATA_FOLDER
from src.core_callbacks import *
from src.callbacks import (callback_views, callback_speckle, callback_compute)
import src.config.logs
from utils.utils import start_compute, start_appserver
from utils.utils_database import execute_sql_file, initial_data_load_from_excel

"""
from src.core_callbacks import *
from src.callbacks import (callback_layout, callback_response, callback_compute)
"""

if __name__ == '__main__':
    # Execute de database model and load initial data
    # execute_sql_file(PATH_DB_MODEL)
    # initial_data_load_from_excel(PATH_DATA_FOLDER)

    # Start the compute.geometry project and the appserver
    # start_compute()
    # start_appserver()
    dash_app.run_server(debug=False, use_reloader=False, port=5000)
