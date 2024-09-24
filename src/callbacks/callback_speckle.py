import logging
import sys
from typing import List, Optional
import dash
import numpy as np
import pandas as pd

from src.core_callbacks import dash_app
from src.utils.utils_plotly import parallel_plot
from src.utils.utils_speckle import merge_commits, update_commit

sys.path.insert(0, '/static/style.py')
sys.path.insert(0, '/apps/utils_plotly.py')
sys.path.insert(0, 'core_callbacks.py')
sys.path.insert(0, 'callbacks/deprecated-utils_speckle.py')


# Speckle callbacks
@dash_app.callback(
    dash.dependencies.Output("speckle-iframe", "src"),
    [dash.dependencies.Input("dropdown_commit", "value"),
     dash.dependencies.Input("dropdown_branches", "value")],
)
def update_latest_commit(dropdown_commit: Optional[str] = None,
                         dropdown_models: Optional[List[str]] = None) -> str:
    merged_url = merge_commits(dropdown_models)
    return merged_url


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


# Plotly callbacks
@dash_app.callback(
    dash.dependencies.Output('speckle_parallel_data', 'figure'),
    [dash.dependencies.Input('store-branches-attributes', 'data')],
    [dash.dependencies.State('speckle_parallel_data', 'figure'),
     ])
def update_parallel_plot(models_attributes_data, par_coord_data):
    """
    Updates the parallel plot based on the selected data in the parallel plot.
    """
    if models_attributes_data is not None:
        if par_coord_data is not None:
            selected_attributes_df_branches = pd.read_json(models_attributes_data,
                                                           orient='split').select_dtypes(
                include=[np.number])

            fig_parallel = parallel_plot(selected_attributes_df_branches)
        else:
            fig_parallel = par_coord_data

        return fig_parallel
    else:
        return {}


@dash_app.callback(
    [dash.dependencies.Output('table_data', 'data'),
     dash.dependencies.Output('dropdown_commit', 'options')],
    [dash.dependencies.Input('speckle_parallel_data', 'figure'),
     dash.dependencies.Input('store-branches', 'data'),
     dash.dependencies.Input('store-branches-attributes', 'data')]
)
def update_table(fig_parallel, selected_commit_metadata, selected_commit_data):
    """
    Updates the table data based on the selected data in the parallel plot.
    Args:
        fig_parallel:
        selected_commit_data:
        selected_commit_metadata:
    """
    try:
        useless_field = ['id', 'totalChildrenCount', 'applicationId']
        if not fig_parallel:
            return [], []

        # Get the selected commit data
        df_obj_data, df_commit_metadata = None, None
        if selected_commit_metadata is not None and selected_commit_data is not None:
            df_commit_metadata = pd.read_json(selected_commit_metadata, orient='split')
            df_obj_data = pd.read_json(selected_commit_data, orient='split').drop(
                columns=useless_field)

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
            for i, col in enumerate(curr_dims):
                dim = col['label']
                if dim in useless_field or dim == 'commitId':
                    continue
                if dim in constraint_range_dict:
                    constraint_range = constraint_range_dict[dim]
                    df = df[(df[dim] >= constraint_range[0]) & (df[dim] <= constraint_range[1])]

        table_data = df_commit_metadata.to_dict('records')
        dropdown_commits = [{'label': i, 'value': i} for i in
                            df_commit_metadata['commitId'].unique()]
        return table_data, dropdown_commits

    except Exception as e:
        logging.exception(e)
        return {}, []
