import logging
import json
import sys
from typing import List, Optional
import dash
import numpy as np
import pandas as pd

from config.settings import useless_fields
from src.core_callbacks import dash_app
from src.utils.utils_plotly import parallel_plot
from src.utils.utils_speckle import merge_commits, update_commit

sys.path.insert(0, '/static/style.py')
sys.path.insert(0, '/apps/utils_plotly.py')
sys.path.insert(0, 'core_callbacks.py')
sys.path.insert(0, 'callbacks/deprecated-utils_speckle.py')


# Merge the selected commits and update the iframe
@dash_app.callback(
    dash.dependencies.Output("speckle-iframe", "src"),
    [dash.dependencies.Input("dropdown_commit", "value"),
     dash.dependencies.Input("dropdown_branches", "value")],
)
def update_latest_commit(dropdown_commit: Optional[str] = None,
                         dropdown_models: Optional[List[str]] = None) -> str:
    merged_url = merge_commits(dropdown_models)
    return merged_url


# Callback related with dropdown and sidebar interactions
@dash_app.callback(
    [dash.dependencies.Output('store-branches', 'data'),
     dash.dependencies.Output('store-branches-attributes', 'data')],
    [dash.dependencies.Input('speckle_data_sidebar', 'n_clicks'),
     dash.dependencies.Input("dropdown_branches", "value")]
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


# Modify the parallel plot based on the selected data
@dash_app.callback(
    dash.dependencies.Output('speckle_parallel_data', 'figure'),
    [dash.dependencies.Input('store-branches-attributes', 'data')],
    [dash.dependencies.State('speckle_parallel_data', 'figure')]
)
def update_parallel_plot(models_attributes_data, par_coord_data):
    """
    Updates the parallel plot based on the selected data in the parallel plot.
    """
    try:
        original_models_attributes = json.loads(models_attributes_data)
        models_attributes = pd.DataFrame(original_models_attributes['data'],
                                         columns=original_models_attributes['columns'])
        if models_attributes.empty:
            raise ValueError("The models_attributes DataFrame is empty.")
        selected_attributes_df_branches: pd.DataFrame = models_attributes
        if len(par_coord_data) != 0:
            selected_points: list = par_coord_data['data'][0].get('selectedpoints', [])
            if len(selected_points) != 0:
                selected_attributes_df_branches = models_attributes.iloc[selected_points]

        fig_parallel = parallel_plot(selected_attributes_df_branches)
        return fig_parallel
    except Exception as e:
        logging.error(e)
        return {}


# Update the table data based on the selected data in the parallel plot
@dash_app.callback(
    [dash.dependencies.Output('table_data', 'data'),
     dash.dependencies.Output('dropdown_commit', 'options')],
    [dash.dependencies.Input('speckle_parallel_data', 'figure'),
     dash.dependencies.Input('store-branches', 'data'),
     dash.dependencies.Input('store-branches-attributes', 'data')],
    [dash.dependencies.State('speckle_parallel_data', 'figure')]
)
def update_table(fig_parallel, selected_commit_metadata, selected_commit_data, fig_state):
    """
    Updates the table data based on the selected data in the parallel plot.
    Args:
        fig_parallel:
        selected_commit_data:
        selected_commit_metadata:
    """
    try:
        if not fig_parallel:
            return [], []

        # Get the selected commit data
        df_commit_metadata = pd.read_json(selected_commit_metadata, orient='split')
        df_obj_data = pd.read_json(selected_commit_data, orient='split')
        if df_commit_metadata.empty or df_obj_data.empty:
            return [], []

        # Clean the dataframe
        df_obj_data = df_obj_data.drop(columns=useless_fields)

        # Get the current dimensions of the parallel plot
        curr_dims = fig_parallel['data'][0].get('dimensions', None)
        # If there is no fig selection
        if 'data' not in fig_parallel or curr_dims is None:
            table_data_original = df_obj_data.to_dict('records')
            dropdown_commits_original = [{'label': i, 'value': i} for i in
                                         df_obj_data['commitId'].unique()]
            return table_data_original, dropdown_commits_original

        # If figure is selected: Get constraint range for each dimension save it in a dict
        constraint_range_dict = {}
        for i, col in enumerate(curr_dims):
            dim = col['label']
            if 'constraintrange' in col:
                constraint_range_dict[dim] = col['constraintrange']

        # Filter the dataframe based on the given ranges in each column
        df = df_obj_data.copy()
        if curr_dims is not None:
            for col in curr_dims:
                dim = col['label']
                # Skip if the column is in useless_fields or is 'commitId'
                if dim in useless_fields or dim == 'commitId':
                    continue
                # Apply range constraints if present
                if dim in constraint_range_dict:
                    min_val, max_val = constraint_range_dict[dim]
                    # Discard rows where values are outside the range
                    df = df.loc[df[dim].between(min_val, max_val)]

        # Get the filtered commit metadata
        table_data = df_commit_metadata[
            df_commit_metadata['commitId'].isin(df['commitId'])].to_dict('records')
        dropdown_commits = [{'label': i, 'value': i} for i in df['commitId'].unique()]
        return table_data, dropdown_commits

    except Exception as e:
        logging.exception(e)
        return {}, []
