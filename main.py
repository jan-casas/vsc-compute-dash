from src.core_callbacks import *
from src.callbacks import (callback_views, callback_speckle, callback_compute)
import src.config.logs
from utils.utils import start_compute, start_appserver

"""
from src.core_callbacks import *
from src.callbacks import (callback_layout, callback_response, callback_compute)
"""

if __name__ == '__main__':
    # start_compute()
    # start_appserver()
    dash_app.run_server(debug=False, use_reloader=False, port=5000)
