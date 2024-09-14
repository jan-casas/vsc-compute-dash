import logging
import sys
from typing import List, Optional

import dash
import pandas as pd
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.wrapper import StreamWrapper

from src.core_callbacks import dash_app
from src.static.style import (CONTENT_STYLE, CONTENT_STYLE1, SIDEBAR_HIDDEN,
                              SIDEBAR_STYLE)
from src.utils import parallel_plot
from src.utils.utils_speckle import client, get_commits, process_commits

sys.path.insert(0, '/static/style.py')
sys.path.insert(0, '/apps/utils_plotly.py')
sys.path.insert(0, 'core_callbacks.py')
sys.path.insert(0, 'callbacks/utils_speckle.py')

# Constants
HOST = 'https://speckle.xyz/'
STREAM_ID = '0e5d383e76'
BRANCH_COMPUTE_TESTING = 'https://speckle.xyz/streams/0e5d383e76/branches/compute%2Ffacade-testing'

# Store the commits per session
store_commits_names = []
store_dict_attributes = {}


# todo: this 2 funcitons must go to utils/speckje
# Callback for the commit management
def get_latest_commit(stream_id: str, client, name_branch: str = 'compute/facade-testing') -> str:
    """
    Gets the latest commit from the stream.

    Args:
        stream_id (str): The stream id.
        client ([type]): The speckle client.
        name_branch (str, optional): The name of the branch. Defaults to 'compute/facade-testing'.

    Returns:
        str: The latest commit.
    """
    branches = client.branch.list(stream_id)
    commits = []
    for branch in branches:
        if branch.__dict__['name'] == name_branch:
            commits = branch.__dict__['commits'].__dict__['items']
            break
    latest_commit = commits[0].__dict__['id']

    return latest_commit


def merge_commits(selected_commits: Optional[List[str]] = None) -> str:
    """
    Merge the base commit and the selected commits into a single dataframe.

    Args:
        selected_commits (Optional[List[str]], optional): The selected commits. Defaults to None.

    Returns:
        str: The url of the iframe.
    """
    # create and authenticate a client
    client = SpeckleClient(host=HOST)
    account = get_default_account()
    client.authenticate_with_account(account)

    # get latest commits from the stream and the base one
    latest_commit, _, _, transport = get_commits(
        stream_id=STREAM_ID, client=client)
    base_commit_url = f"https://speckle.xyz/streams/{STREAM_ID}/commits/36680e09fb"
    commits = [base_commit_url]

    if selected_commits is None:
        latest_commit_url = f"https://speckle.xyz/streams/{STREAM_ID}/commits/9c2637ae37"
        commits.append(latest_commit_url)
    else:
        for selected_commit in selected_commits:
            selected_commit_url = f"https://speckle.xyz/streams/{STREAM_ID}/commits/{selected_commit}"
            commits.append(selected_commit_url)

    print("Commits:", commits)

    # create a list of stream wrappers (the stream wrapper is a wrapper around the commit object)
    wrappers = [StreamWrapper(commit_url) for commit_url in commits]
    stream_id = wrappers[0].stream_id
    commit_ids = [wrapper.commit_id for wrapper in wrappers]

    # the overlay is for all commits after the first in the array
    overlay = ",".join(commit_ids[1:])

    embed_url = (f"https://speckle.xyz/embed?stream={stream_id}&commit={commit_ids[0]}&overlay="
                 f"{overlay}&transparent=true&autoload=true&hidecontrols=true&hidesidebar=true&hideselectioninfo=false")

    return embed_url


@dash_app.callback(
    dash.dependencies.Output("speckle-iframe", "src"),
    [dash.dependencies.Input("dropdown_commit", "value"),
     dash.dependencies.Input("dropdown_branches", "value")],
)
def update_latest_commit(dropdown_commit: Optional[str] = None, dropdown_branches: Optional[List[str]] = None) -> str:
    """Updates the iframe with the latest commit.

    :param dropdown_commit: The selected branch.
    :type dropdown_commit: str
    :param dropdown_branches: The selected commits.
    :type dropdown_branches: List[str]
    :return: The url of the iframe.
    """
    # if dropdown_commit is None:
    #     merged_url = merge_commits()
    # else:
    # TODO: Get the commit id before merge commits (dropdown_branches)
    latest_commit_id_branch_selected = []
    if dropdown_branches is not None:
        for branch in dropdown_branches:
            latest_commit_id_branch_selected.append(get_latest_commit(STREAM_ID, client, name_branch=branch))

    dropdowns_values = latest_commit_id_branch_selected + [
        dropdown_commit] if dropdown_commit is not None else latest_commit_id_branch_selected
    print("The list of commits is:", dropdowns_values)
    merged_url = merge_commits(selected_commits=dropdowns_values)
    return merged_url


def update_branch_commits():
    """
    Updates the branch commits.

    :return: The branch commits.
    """
    logging.info("Updated branch commits")
    try:
        # Initialize speckle login
        latest_commit, commits, commit_data, transport = get_commits(stream_id=STREAM_ID, client=client, limit=10)
        new_commits = [commit for commit in commit_data if commit['id'] not in store_commits_names]
        # Initialize the dicts
        if len(store_commits_names) == 0:
            dict_attributes = process_commits(commits, transport)
            store_dict_attributes.update(dict_attributes)
            store_commits_names.extend(commit['id'] for commit in new_commits)
        # Update the dicts with the new commits
        if new_commits:
            dict_attributes = process_commits(new_commits, transport)
            store_dict_attributes.update(dict_attributes)
            store_commits_names.extend(commit['id'] for commit in new_commits)

        data_dict = {k: v[0] for k, v in store_dict_attributes.items()}
        df_branches = pd.DataFrame.from_dict(data_dict, orient='index')

        if all(isinstance(col, str) for col in df_branches.columns):
            selected_attributes_df_branches = df_branches.loc[:, df_branches.columns.str.contains('@')]
        else:
            return None, None

        return df_branches, selected_attributes_df_branches
    except Exception as e:
        logging.exception(e)
        return None, None


@dash_app.callback(
    [dash.dependencies.Output('store-branches', 'data'),
     dash.dependencies.Output('store-branches-attributes', 'data')],
    [dash.dependencies.Input('speckle_data_sidebar', 'n_clicks')]
    # [dash.dependencies.State("collapse", "is_open")]
)
def update_data(n_clicks):
    logging.info("Updated data n_clicks %s", n_clicks)
    if n_clicks is not None:
        df_branches, selected_attributes_df_branches = update_branch_commits()
        if df_branches is not None and selected_attributes_df_branches is not None:
            return df_branches.to_json(date_format='iso', orient='split'), selected_attributes_df_branches.to_json(
                date_format='iso', orient='split')
    return None, None


# Callback for the Speckle OP Panel
@dash_app.callback(
    dash.dependencies.Output('speckle_parallel_data', 'figure'),
    [dash.dependencies.Input('speckle_parallel_data', 'restyleData'),
     dash.dependencies.Input('store-branches-attributes', 'data')],
    [dash.dependencies.State('speckle_parallel_data', 'figure'),
     ])
def update_parallel_plot(restyledata, branches_attributes_data, par_coord_data):
    """
    Updates the parallel plot based on the selected data in the parallel plot.

    :param restyledata: The restyle data.
    :type restyledata: dict
    :param par_coord_data: The parallel plot data.
    :type par_coord_data: dict
    :return: The parallel plot figure.
    """
    logging.info("Updated parallel plot")
    if branches_attributes_data is not None:
        if par_coord_data is None or len(par_coord_data) == 0:
            selected_attributes_df_branches = pd.read_json(branches_attributes_data, orient='split')
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
def update_table(fig_parallel, branches_data, branches_attributes_data):
    """
    Updates the table data based on the selected data in the parallel plot.

    :param fig_parallel: The parallel plot figure.
    :type fig_parallel: dict
    :return: The table data.
    """
    logging.info("Updated table data")

    try:
        if branches_data is not None and branches_attributes_data is not None:
            df_branches = pd.read_json(branches_data, orient='split')
            selected_attributes_df_branches = pd.read_json(branches_attributes_data, orient='split')

        if 'data' not in fig_parallel:
            return {}, []
        curr_dims = fig_parallel['data'][0].get('dimensions', None)

        # Get constraintrange for each dimension save it in a dict
        constraintrange_dict = {}
        for i, col in enumerate(curr_dims):
            dim = col['label']
            if 'constraintrange' in col:
                constraintrange_dict[dim] = col['constraintrange']

        # Filter the dataframe based on the given ranges in each colunm
        filtered_df = selected_attributes_df_branches.copy()
        for i, col in enumerate(curr_dims):
            dim = col['label']
            if dim in constraintrange_dict:
                constraintrange = constraintrange_dict[dim]
                filtered_df = filtered_df[(filtered_df[dim] >= constraintrange[0]) & (
                        filtered_df[dim] <= constraintrange[1])]

        try:
            filtered_df_only_commit = df_branches.loc[
                filtered_df.index, ['authorName', 'commitId', 'message']]
            return filtered_df_only_commit.to_dict('records'), [{'label': i, 'value': i} for i in
                                                                filtered_df_only_commit['commitId'].unique()]

        except:
            return {}, []

    except Exception as e:
        logging.exception(e)
        return {}, []


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

    :param n1: The number of times the button has been clicked.
    :type n1: int
    :param n2: The number of times the button has been clicked.
    :type n2: int
    :param nclick: The number of times the button has been clicked.
    :type nclick: str
    :return: The sidebar style, the content style and the number of times the button has been clicked.
    """
    ctx = dash.callback_context

    if not ctx.triggered:
        sidebar_style = SIDEBAR_HIDDEN
        content_style = CONTENT_STYLE
        cur_nclick = 'HIDDEN'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'speckle_data_sidebar' and n1:
            if nclick == "SHOW":
                sidebar_style = SIDEBAR_HIDDEN
                content_style = CONTENT_STYLE1
                cur_nclick = "HIDDEN"
            else:
                sidebar_style = SIDEBAR_STYLE
                content_style = CONTENT_STYLE
                cur_nclick = "SHOW"
        elif button_id == 'update_speckle_iframe' and n2:  # Add this condition
            sidebar_style = SIDEBAR_HIDDEN
            content_style = CONTENT_STYLE
            cur_nclick = 'HIDDEN'

    return sidebar_style, content_style, cur_nclick
