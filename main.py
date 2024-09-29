import subprocess
import logging

from src.core_callbacks import *
from src.callbacks import (callback_views, callback_speckle, callback_compute)
import src.config.logs

"""
import subprocess
from src.core_callbacks import *
from src.callbacks import (callback_layout, callback_response, callback_compute)
"""


def start_compute(
        path=r'C:\Users\casas\AppData\Roaming\McNeel\Rhinoceros\packages\7.0\Hops\0.16.2\compute'
             r'.geometry\compute.geometry.exe'):
    """
    Starts the compute.geometry project in a separate process.
    """
    try:
        subprocess.Popen(path)
        logging.info('Started compute.geometry')
    except FileNotFoundError:
        logging.error(f"Failed to start compute.geometry. File not found: {path}")
    except Exception as e:
        logging.error(f"Failed to start compute.geometry. Error: {str(e)}")


def start_appserver(node_path=r'C:\Program Files\nodejs\node.exe',
                    npm_path=r'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js',
                    appserver_path=r'G:\vsc-compute-appserver'):
    """
    Starts the other project in a separate process. This is needed because the other project is a
    node.js project.
    """
    # Start the appserver before compute is loaded
    subprocess.Popen([node_path, npm_path, 'start'], cwd=appserver_path)
    logging.info('Started appserver')


if __name__ == '__main__':
    # start_compute()
    # start_appserver()
    dash_app.run_server(debug=True, use_reloader=False, port=5000)
