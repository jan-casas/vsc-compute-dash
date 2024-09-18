import logging
import time

import dash
import openai

from src.config.settings import OPENAI_API_KEY
from src.core_callbacks import dash_app


@dash_app.callback(
    dash.dependencies.Output("positioned-toast", "is_open"),
    [dash.dependencies.Input("update_speckle_iframe", "n_clicks")],
)
def toggle_toast(n):
    """
    Toggles the toast.

    :param n: The number of times the button has been clicked.
    :type n: int
    :return: The toast.
    """
    time.sleep(3)
    if n > 0:
        return True
    return False


# Callback for modals
@dash_app.callback(
    dash.dependencies.Output("modal", "is_open"),
    [dash.dependencies.Input("open_chat_button", "n_clicks")],
    [dash.dependencies.State("modal", "is_open")],
)
def toggle_modal(n1, is_open):
    """
    Toggles the modal.

    :param n1: The number of times the button has been clicked.
    :type n1: int
    :param is_open: The modal state.
    :type is_open: bool
    :return: The modal.
    """
    if n1:
        return not is_open
    return is_open


@dash_app.callback(
    dash.dependencies.Output("help_modal", "is_open"),
    [dash.dependencies.Input("open_help_button", "n_clicks")],
    [dash.dependencies.State("help_modal", "is_open")],
)
def toggle_modal_help(n1, is_open):
    """
    Toggles the modal.

    :param n1: The number of times the button has been clicked.
    :type n1: int
    :param is_open: The modal state.
    :type is_open: bool
    :return: The modal.
    """
    if n1:
        return not is_open
    return is_open


# Callback for the collapse
@dash_app.callback(
    dash.dependencies.Output("collapse", "is_open"),
    [dash.dependencies.Input("update_speckle_iframe", "n_clicks"),
     dash.dependencies.Input("bake-button", "n_clicks"),
     dash.dependencies.Input("speckle_data_sidebar", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")],
)
def toggle_collapse(n1, n2, n3, is_open):
    """
    Toggles the collapse.

    :param n1: The number of times the button has been clicked.
    :type n1: int
    :param n2: The number of times the button has been clicked.
    :type n2: int
    :param n3: The number of times the button has been clicked.
    :type n3: int
    :param is_open: The collapse state.
    :type is_open: bool
    :return: The collapse.
    """
    print('Toggle Collapse')
    ctx = dash.callback_context

    if not ctx.triggered:
        return is_open
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'update_speckle_iframe' and n1:
        return not is_open
    elif button_id == 'bake-button' and n2:
        return False
    elif button_id == 'speckle_data_sidebar' and n3:  # Add this condition
        return False if is_open else is_open  # Close the collapse if it's open, otherwise leave
        # it as is
    return is_open


# Random commit message suggestion
def openai_chat(prompt, model="gpt-3.5-turbo", temperature=0.5):
    openai.api_key = OPENAI_API_KEY
    try:
        messages = [{"role": "user", "content": prompt}]
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


@dash_app.callback(
    dash.dependencies.Output('input_commit_message', 'value'),
    dash.dependencies.Input('update_speckle_iframe', 'n_clicks'),
)
def get_random_message(n_clicks):
    if n_clicks is not None:
        commit_message = (openai_chat(
            "Create a random funny and short git commit message. (max 20 words)")
                          .replace("'", "").replace('"', ''))
        return commit_message
    return None
