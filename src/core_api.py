"""
API to communicate values modified in the webapp to the Rhino Compute server. This API is used to update the slider.

"""

import psycopg2
from flask import jsonify, request

from core_callbacks import *
from src.config.settings import DATABASE, DB_PASSWORD, DB_USER, HOST, PORT


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


@app.route('/api/slider_values', methods=['POST', 'GET'])
def update_slider_values():
    """
    Endpoint for updating the slider values in the database. If the request is a POST request, the slider values are
    updated in the database. If the request is a GET request, the latest slider values are retrieved from the database.
    """
    # If POST request, update the slider values in the database
    if request.method == 'POST':
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'No data provided'}), 400
        slider_values = data.get('slider-values-store')
        if slider_values is None:
            return jsonify({'error': 'No slider values provided'}), 400

        try:
            # Connect to the database
            with psycopg2.connect(host=HOST, database=DATABASE, user=DB_USER, password=DB_PASSWORD, port=PORT) as conn:
                with conn.cursor() as cur:
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
                        VALUES (%s, %s, %s, %s)
                    """, (slider_values['radius'], slider_values['count'], slider_values['span'],
                          slider_values['commit_message']))
        except psycopg2.Error as e:
            return jsonify({'error': 'Database error: {}'.format(e.pgerror)}), 500

        return jsonify({'message': 'Slider values updated successfully'})

    # If GET request, get the latest slider values from the database
    elif request.method == 'GET':
        try:
            # Connect to the database
            with psycopg2.connect(host=HOST, database=DATABASE, user=DB_USER, password=DB_PASSWORD, port=PORT) as conn:
                with conn.cursor() as cur:
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
        except psycopg2.Error as e:
            return jsonify({'error': 'Database error: {}'.format(e.pgerror)}), 500

    else:
        return jsonify({'error': 'Method not allowed'}), 405
