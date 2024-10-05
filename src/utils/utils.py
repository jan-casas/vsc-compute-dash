import subprocess

import openai
import logging

from src.config.settings import OPENAI_API_KEY, COMPUTE_PATHS


def start_compute():
    """
    Starts the compute.geometry project in a separate process.
    """
    compute_path = COMPUTE_PATHS['compute']

    try:
        subprocess.Popen(compute_path, shell=True)
        logging.info('Started compute.geometry')
    except FileNotFoundError:
        logging.error(f"Failed to start compute.geometry. File not found: {compute_path}")
    except Exception as e:
        logging.error(f"Failed to start compute.geometry. Error: {str(e)}")


def start_appserver():
    """
    Starts the other project in a separate process. This is needed because the other project is a
    node.js project.
    """
    node_path = COMPUTE_PATHS['node']
    npm_path = COMPUTE_PATHS['npm']
    appserver_path = COMPUTE_PATHS['appserver']

    try:
        subprocess.Popen([node_path, npm_path, 'start'], cwd=appserver_path, shell=True)
        logging.info('Started appserver')
    except FileNotFoundError:
        logging.error(f"Failed to start appserver. File not found: {appserver_path}")
    except Exception as e:
        logging.error(f"Failed to start appserver. Error: {str(e)}")


# Random commit message suggestion
def openai_chat(prompt, model="gpt-3.5-turbo", temperature=0.5):
    openai.api_key = OPENAI_API_KEY
    try:
        messages = [{"role": "user", "content": prompt.replace("'", "").replace('"', '')}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        r = response.choices[0].message["content"]
        return r
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
