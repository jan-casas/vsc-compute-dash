import logging
from io import StringIO
from typing import List, Optional
import dash
import plotly.express as px
import pandas as pd

from config.settings import UNWANTED_FIELDS
from src.core_callbacks import dash_app
from src.utils.utils_speckle import merge_commits, update_commit


# Callback related with dropdown and sidebar interactions
@dash_app.callback(
    [dash.dependencies.Output('store-branches', 'data'),
     dash.dependencies.Output('store-branches-attributes', 'data')],
    [dash.dependencies.Input('speckle-data-sidebar', 'n_clicks'),
     dash.dependencies.Input("dropdown-branches", "value")]
    # [dash.dependencies.State("collapse", "is_open")]
)
def update_data(n_clicks, dropdown_models):
    selected_model = next(
        (model for model in dropdown_models if model.startswith('compute/')), None)

    if n_clicks is None or selected_model is None:
        return None, None

    else:
        selected_model = [selected_model] if not isinstance(selected_model,
                                                            list) else selected_model
        selected_commit_metadata, selected_commit_data = update_commit(selected_model)
        if selected_commit_metadata is not None and selected_commit_data is not None:
            data_store_branches = selected_commit_metadata.to_json(
                date_format='iso', orient='split')
            data_store_branches_attributes = selected_commit_data.to_json(
                date_format='iso', orient='split')

            return data_store_branches, data_store_branches_attributes


# Merge the selected commits and update the iframe
@dash_app.callback(
    dash.dependencies.Output("speckle-iframe", "src"),
    [dash.dependencies.Input("dropdown-branches", "value")],
)
def update_latest_commit(dropdown_models: Optional[List[str]] = None) -> str:
    merged_url = merge_commits(dropdown_models)
    return merged_url


# Update the parcoords plot based on the original data
@dash_app.callback(
    dash.dependencies.Output('parcoords-plot', 'figure'),
    [dash.dependencies.Input('store-branches-attributes', 'data')]
)
def update_parallel_plot(selected_commit_data):
    """
    Updates the parallel coordinates plot based on the original data.
    """
    try:
        if selected_commit_data is None:
            return {}
        df_obj_data = pd.read_json(StringIO(selected_commit_data), orient='split')
        df_obj_data = df_obj_data.drop(columns=UNWANTED_FIELDS)
        if df_obj_data.empty:
            return {}
        else:
            fig = px.parallel_coordinates(df_obj_data, dimensions=df_obj_data.columns)
            return fig

    except Exception as e:
        logging.error(e)
        return {}


# Update the table based on interactions with the parcoords plot
@dash_app.callback(
    [dash.dependencies.Output('filtered-table', 'data'),
     dash.dependencies.Output('dropdown-commit', 'options')],
    [dash.dependencies.Input('parcoords-plot', 'restyleData'),
     dash.dependencies.Input('store-branches', 'data'),
     dash.dependencies.Input('store-branches-attributes', 'data')],
    [dash.dependencies.State('parcoords-plot', 'figure')]
)
def update_table(restyleData, selected_commit_metadata, selected_commit_data, figure):
    """
    Updates the table data and dropdown options based on the selected data in the parallel plot.
    """
    try:
        if selected_commit_metadata is None or selected_commit_data is None:
            return [], []

        # Convert JSON strings to DataFrames
        df_commit_metadata = pd.read_json(StringIO(selected_commit_metadata), orient='split')
        df_obj_data = pd.read_json(StringIO(selected_commit_data), orient='split')
        df_obj_data = df_obj_data.drop(columns=UNWANTED_FIELDS, errors='ignore')

        if df_commit_metadata.empty or df_obj_data.empty:
            return [], []

        # If no data is selected, return the original data
        if not restyleData or not figure or 'data' not in figure or len(figure['data']) == 0:
            table_data_original = df_obj_data.to_dict('records')
            dropdown_commits_original = [{'label': i, 'value': i} for i in
                                         df_obj_data['commitId'].unique()]
            return table_data_original, dropdown_commits_original

        # Filter the data based on the selected ranges
        filtered_df = df_obj_data.copy()

        # Iterate over the dimensions to apply filters
        for dim_data in figure['data'][0]['dimensions']:
            dim_label = dim_data.get('label')
            dim_range = dim_data.get('constraintrange')

            if dim_label and dim_range:
                if isinstance(dim_range[0], list):  # Handle multiple selection ranges
                    mask = pd.Series([False] * len(filtered_df))
                    for r in dim_range:
                        mask |= (filtered_df[dim_label] >= r[0]) & (filtered_df[dim_label] <= r[1])
                    filtered_df = filtered_df[mask]
                else:  # Single selection range
                    filtered_df = filtered_df[
                        (filtered_df[dim_label] >= dim_range[0]) &
                        (filtered_df[dim_label] <= dim_range[1])
                        ]

        # Filter the commit metadata based on the filtered commit IDs
        table_data = df_commit_metadata[
            df_commit_metadata['commitId'].isin(filtered_df['commitId'])].to_dict('records')
        dropdown_commits = [{'label': i, 'value': i} for i in filtered_df['commitId'].unique()]

        return table_data, dropdown_commits

    except Exception as e:
        logging.exception(e)
        return [], []
