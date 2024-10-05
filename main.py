from config.settings import COMPUTE_PATHS
from src.core_callbacks import *
from src.callbacks import (callback_views, callback_speckle, callback_compute)
import src.config.logs
from utils.utils import start_compute, start_appserver

"""
import subprocess
from src.core_callbacks import *
from src.callbacks import (callback_layout, callback_response, callback_compute)
"""

if __name__ == '__main__':
    # start_compute()
    # start_appserver()
    dash_app.run_server(debug=True, use_reloader=False, port=5000)
