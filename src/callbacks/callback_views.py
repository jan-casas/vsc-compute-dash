import dash

from src.core_callbacks import dash_app
from static.style import sidebar_hidden_dict, content_style_dict, content_style1_dict, \
    sidebar_style_dict


# Callback for the collapse
@dash_app.callback(
    dash.dependencies.Output("collapse", "is_open"),
    [dash.dependencies.Input("update-speckle-iframe", "n_clicks"),
     dash.dependencies.Input("bake-button", "n_clicks"),
     dash.dependencies.Input("speckle-data-sidebar", "n_clicks")],
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

    if button_id == 'update-speckle-iframe' and n1:
        return not is_open
    elif button_id == 'bake-button' and n2:
        return False
    elif button_id == 'speckle-data-sidebar' and n3:  # Add this condition
        return False if is_open else is_open  # Close the collapse if it's open, otherwise leave
        # it as is
    return is_open


@dash_app.callback(
    [
        dash.dependencies.Output("sidebar-data", "style"),
        dash.dependencies.Output("page-content", "style"),
        dash.dependencies.Output("side-click", "data"),
        dash.dependencies.Output("sidebar-components", "style"),
        dash.dependencies.Output("non-static-header", "children")
    ],
    [
        dash.dependencies.Input("dropdown-commit", "value"),
        dash.dependencies.Input("speckle-data-sidebar", "n_clicks"),
        dash.dependencies.Input("speckle-data-count", "n_clicks"),
        dash.dependencies.Input("update-speckle-iframe", "n_clicks")
    ],
    [dash.dependencies.State("side-click", "data")]
)
def toggle_sidebar(commit_id, n1, n2, n3, sidebar_states):
    """
    Toggles the sidebars such that activating one hides the other.
    """
    ctx = dash.callback_context

    # Initialize the sidebar states if None
    if sidebar_states is None:
        sidebar_states = {'sidebar_data': 'HIDDEN', 'sidebar_components': 'HIDDEN'}

    # Default styles (hidden)
    sidebar_style = sidebar_hidden_dict
    new_sidebar_style = sidebar_hidden_dict
    content_style = content_style_dict
    title = "Quantitative Analysis for the commitId None"

    if not ctx.triggered:
        return sidebar_style, content_style, sidebar_states, new_sidebar_style, title

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'speckle-data-sidebar' and n1:
        # Toggle sidebar-data
        if sidebar_states.get('sidebar_data') == 'SHOW':
            # Hide sidebar-data
            sidebar_style = sidebar_hidden_dict
            content_style = content_style1_dict
            sidebar_states['sidebar_data'] = 'HIDDEN'
        else:
            # Show sidebar-data and hide sidebar-components
            sidebar_style = sidebar_style_dict
            new_sidebar_style = sidebar_hidden_dict
            content_style = content_style_dict
            sidebar_states['sidebar_data'] = 'SHOW'
            sidebar_states['sidebar_components'] = 'HIDDEN'

    elif button_id == 'speckle-data-count' and n2:
        # Toggle sidebar-components
        if sidebar_states.get('sidebar_components') == 'SHOW':
            # Hide sidebar-components
            new_sidebar_style = sidebar_hidden_dict
            content_style = content_style1_dict
            sidebar_states['sidebar_components'] = 'HIDDEN'
            title = f'Quantitative Analysis for the commitId {commit_id}'
        else:
            # Show sidebar-components and hide sidebar-data
            new_sidebar_style = sidebar_style_dict
            sidebar_style = sidebar_hidden_dict
            content_style = content_style_dict
            sidebar_states['sidebar_components'] = 'SHOW'
            sidebar_states['sidebar_data'] = 'HIDDEN'

    elif button_id == 'update-speckle-iframe' and n3:
        # Hide both sidebars
        sidebar_style = sidebar_hidden_dict
        new_sidebar_style = sidebar_hidden_dict
        content_style = content_style_dict
        sidebar_states['sidebar_data'] = 'HIDDEN'
        sidebar_states['sidebar_components'] = 'HIDDEN'

    return sidebar_style, content_style, sidebar_states, new_sidebar_style, title
