import logging

import dash
import requests

from src.core_callbacks import dash_app


@dash_app.callback(
    dash.dependencies.Output('slider-values-store', 'data'),  # Add this line
    [dash.dependencies.Input('compute-span-slider', 'value'),
     dash.dependencies.Input('compute-count-slider', 'value'),
     dash.dependencies.Input('compute-radius-slider', 'value'),
     dash.dependencies.Input('input_commit_message', 'value')]
)
def update_slider_values_store(span, count, radius, message) -> dict:
    """
    This callback updates the slider values store with the values from the sliders.

    Args:
        span: Value of the span slider
        count: Value of the count slider
        radius: Value of the radius slider
        message: Value of the commit message input

    Returns:
        A dictionary with the slider values
    """
    slider_values = {'count': count, 'radius': radius, 'span': span, 'commit_message': message}
    logging.info(slider_values)
    return slider_values


@dash_app.callback(
    dash.dependencies.Output('dummy-output', 'children'),
    [dash.dependencies.Input('bake-button', 'n_clicks')],
    [dash.dependencies.State('slider-values-store', 'data')]
)
def update_slider_values(n_clicks, data):
    """
    This callback sends the slider values to the compute.app.

    Args:
        n_clicks: Number of clicks on the bake button
        data: The slider values

    Returns:
        None
    """
    if n_clicks is not None:
        requests.post('http://localhost/api/slider_values', json={'slider-values-store': data})
