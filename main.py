import subprocess
from src.core_api import *
from src.core_callbacks import *
from callbacks import (callback_layout, callback_response)


# from callbacks import (callback_layout, callback_response)

def start_other_project(node_path=r'C:\Program Files\nodejs\node.exe',
                        npm_path=r'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js',
                        appserver_path=r'G:\vsc-compute-appserver'):
    """
    Starts the other project in a separate process. This is needed because the other project is a
    node.js project.
    """
    subprocess.Popen([node_path, npm_path, 'start'], cwd=appserver_path)
    # FIXME: Cambiar ip local del compute.rhino3d.appserver (archivo script.js and app.js)


if __name__ == '__main__':
    # TODO: This is a hack. It should be started in a separate container (Windows VM). You mus t
    #  change the ip of the compute.rhino3d.appserver to the ip of the Flask application.
    # start_other_project()

    app.run(debug=False, host='0.0.0.0', port=80)
