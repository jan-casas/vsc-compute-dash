import logging
import requests
import sqlite3

import dash
from flask import jsonify, request

from src.core_callbacks import app, dash_app


# Interaction with the sliders values
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
def update_slider_values(n_clicks, slider_data):
    """
    This callback sends the slider values to the compute.app.

    Args:
        n_clicks: Number of clicks on the bake button
        slider_data: The slider values

    Returns:
        None
    """
    if n_clicks is not None:
        requests.post('http://127.0.0.1:80/api/slider_compute',
                      json={'slider-values-store': slider_data})


# Endpoints API compute.webapp
@app.route('/api/health', methods=['GET'])
def healthcheck():
    """
    Healthcheck endpoint
    """
    return jsonify({'status': 'ok'})


# Endpoints API compute.webapp
dash_app.clientside_callback(
    """
    function(data) {
        document.getElementById('bake-button').click();
    }
    """,
    dash.dependencies.Output('bake-button', 'n_clicks'),
    [dash.dependencies.Input('slider-values-store', 'data')]
)


def post_slider_values(cur):
    # If POST request, update the slider values in the database
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No data provided'}), 400
    slider_values = data.get('slider-values-store')
    if slider_values is None:
        return jsonify({'error': 'No slider values provided'}), 400

    try:
        # Create the table if it doesn't exist
        cur.execute("""
                CREATE TABLE IF NOT EXISTS slider_values (
                    id SERIAL PRIMARY KEY,
                    radius INTEGER,
                    counte INTEGER,
                    span INTEGER,
                    commit_message TEXT
                )
            """)

        # Insert the slider values into the table
        cur.execute("""
                INSERT INTO slider_values (radius, counte, span, commit_message)
                VALUES (?, ?, ?, ?)
            """, (slider_values['radius'], slider_values['count'], slider_values['span'],
                  slider_values['commit_message']))
        cur.connection.commit()
        logging.info('Slider values updated successfully')
        return jsonify({'status': 'success'}), 200
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error: {}'.format(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Error: {}'.format(e)}), 500


def get_slider_values(cur):
    try:
        # Select the latest slider values from the table
        cur.execute("""
            SELECT radius, counte, span, commit_message
            FROM slider_values
            ORDER BY id DESC
            LIMIT 1
        """)
        result = cur.fetchone()
        if result is None:
            return jsonify({'error': 'No slider values found'}), 404
        radius_value, counte_value, span_value, commit_message = result
        return jsonify({'radius': radius_value, 'counte': counte_value, 'span': span_value,
                        'commit_message': commit_message}), 200
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error: {}'.format(e)}), 500


@app.route('/api/slider_compute', methods=['POST', 'GET', 'OPTIONS'])
def update_slider_values():
    """
    Endpoint for updating the slider values in the database. If the request is a POST request,
    the slider values are updated in the database. If the request is a GET request, the latest
    slider values are retrieved from the database.
    """
    if request.method == 'OPTIONS':
        # Handle preflight request
        return jsonify({'status': 'CORS preflight successful'}), 200

    # Connect to the SQLite database
    conn = sqlite3.connect('compute.db')
    cur = conn.cursor()

    if request.method == 'POST':
        response = post_slider_values(cur)
    elif request.method == 'GET':
        response = get_slider_values(cur)
    else:
        response = jsonify({'error': 'Invalid request method'}), 405

    conn.close()
    return response
