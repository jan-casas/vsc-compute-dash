import subprocess

from src.core_api import *


def start_other_project(node_path=r'C:\Program Files\nodejs\node.exe',
                        npm_path=r'C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js',
                        appserver_path=r'C:\Users\casas\OneDrive\compute.rhino3d.appserver'):
    """
    Starts the other project in a separate process. This is needed because the other project is a node.js project.

    Args:
        node_path: Path to node.exe
        npm_path: Path to npm-cli.js
        appserver_path: Path to the appserver folder

    Returns:
        None
    """
    subprocess.Popen([node_path, npm_path, 'start'], cwd=appserver_path)
    # FIXME: Cambiar ip local del compute.rhino3d.appserver (archivo script.js and app.js)


if __name__ == '__main__':
    # 1. Ejecutar Rhino Compute en Local (Esto debería estar ejecutando en una VM de Windows)
    # 2. Cambiar las ip del compute.rhino3d.appserver a la ip de la ip de la aplicacción de Flask
    start_other_project()  # TODO: This is a hack. It should be started in a separate container.
    app.run(debug=False, host='0.0.0.0', port=80)
