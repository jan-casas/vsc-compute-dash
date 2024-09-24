import subprocess
from src.core_callbacks import *
from src.callbacks import (callback_views, callback_speckle, callback_compute)

"""
import subprocess
from src.core_callbacks import *
from src.callbacks import (callback_layout, callback_response, callback_compute)
"""


def start_compute(
        path=r'C:\Users\casas\AppData\Roaming\McNeel\Rhinoceros\packages\7.0\Hops\0.16.2\rhino'
             r'.compute\rhino.compute.exe'):
    """
    Starts the compute project in a separate process.
    """
    subprocess.Popen(path)
    logging.info('Started compute')


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
    app.run(debug=False, host='0.0.0.0', port=80)
