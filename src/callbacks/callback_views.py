import time

import dash

from src.core_callbacks import dash_app
from static.style import sidebar_hidden_dict, content_style_dict, content_style1_dict, \
    sidebar_style_dict
from utils.utils import openai_chat


# @dash_app.callback(
#     dash.dependencies.Output("positioned-toast", "is_open"),
#     [dash.dependencies.Input("update_speckle_iframe", "n_clicks")],
# )
# def toggle_toast(n):
#     """
#     Toggles the toast.
#
#     :param n: The number of times the button has been clicked.
#     :type n: int
#     :return: The toast.
#     """
#     time.sleep(3)
#     if n > 0:
#         return True
#     return False


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
    """
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


# @dash_app.callback(
#     dash.dependencies.Output('input_commit_message', 'value'),
#     dash.dependencies.Input('update_speckle_iframe', 'n_clicks'),
# )
# def get_random_message(n_clicks):
#     if n_clicks is not None:
#         commit_message = (openai_chat(
#             "Create a random funny and short git commit message. (max 20 words)"))
#         return commit_message
#     return None


@dash_app.callback(
    [
        dash.dependencies.Output("sidebar_data", "style"),
        dash.dependencies.Output("page-content", "style"),
        dash.dependencies.Output("side_click", "data")],
    [dash.dependencies.Input("speckle_data_sidebar", "n_clicks"),
     dash.dependencies.Input("update_speckle_iframe", "n_clicks")],  # Add this line
    [dash.dependencies.State("side_click", "data")]
)
def toggle_sidebar(n1, n2, nclick):  # Add n2 to the function parameters
    """
    Toggles the sidebar.
    """
    ctx = dash.callback_context

    sidebar_style, content_style, cur_nclick = None, None, None
    if not ctx.triggered:
        sidebar_style = sidebar_hidden_dict
        content_style = content_style_dict
        cur_nclick = 'HIDDEN'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'speckle_data_sidebar' and n1:
            if nclick == "SHOW":
                sidebar_style = sidebar_hidden_dict
                content_style = content_style1_dict
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = sidebar_style_dict
                content_style = content_style_dict
                cur_nclick = "SHOW"
        elif button_id == 'update_speckle_iframe' and n2:  # Add this condition
            sidebar_style = sidebar_hidden_dict
            content_style = content_style_dict
            cur_nclick = 'HIDDEN'

    return sidebar_style, content_style, cur_nclick
