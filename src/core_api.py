"""
API to communicate values modified in the webapp to the Rhino Compute server. This API is used to
update the slider.

"""
import logging
import sqlite3

import dash
from flask import jsonify

from core_callbacks import app, dash_app

conn = sqlite3.connect('compute.db')


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


def post_slider_values(cur, request):
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
        conn.commit()
        logging.info('Slider values updated successfully')
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error: {}'.format(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Slider values updated successfully'})


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
                        'commit_message': commit_message})
    except sqlite3.Error as e:
        return jsonify({'error': 'Database error: {}'.format(e)}), 500
    finally:
        conn.close()


@app.route('/api/slider_values', methods=['POST', 'GET'])
def update_slider_values(request):
    """
    Endpoint for updating the slider values in the database. If the request is a POST request,
    the slider values are
    updated in the database. If the request is a GET request, the latest slider values are
    retrieved from the database.
    """
    # Connect to the SQLite database
    cur = conn.cursor()
    logging.info('Connected to the database')

    if request.method == 'POST':
        return post_slider_values(cur, request)
    # If GET request, get the latest slider values from the database
    elif request.method == 'GET':
        return get_slider_values(cur)

    else:
        return jsonify({'error': 'Method not allowed'}), 405
