import sys
import warnings

import pandas as pd
import plotly.graph_objects as go

from config.settings import useless_fields

sys.path.insert(0, 'core_callbacks.py')
pd.options.mode.chained_assignment = None
warnings.simplefilter(action='ignore', category=FutureWarning)


def create_table(df_branches):
    """
    Creates a table with the branches data

    Args:
        df_branches: dataframe with the branches data

    Returns:
        fig_commits: figure with the table
        fig_branches: figure with the table
    """
    df_commits = pd.DataFrame(columns=df_branches.keys())

    # Graphs for the commits
    table_commits = go.Table(
        header=dict(values=list(df_commits.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_commits[col] for col in df_commits.columns],
                   fill_color='lavender',
                   align='left'))

    table_branches = go.Table(
        header=dict(values=list(df_branches.columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df_branches[col] for col in df_branches.columns],
                   fill_color='lavender',
                   align='left'))

    fig_commits = go.Figure(data=table_commits)
    fig_branches = go.Figure(data=table_branches)

    return fig_commits, fig_branches


def parallel_plot(df_branches: pd.DataFrame, selected_data: list = None, ui_revision=None):
    """
    Creates a parallel plot with the branches data

    Args:
        df_branches (dataframe): dataframe with the branches data
        selected_data (list): data selected from the parallel plot
        ui_revision (str): revision of the parallel plot

    Returns:
        fig: figure with the parallel plot
    """
    df_branches_selected = df_branches.drop(columns=useless_fields, errors='ignore')

    if selected_data is not None:
        df_selected = pd.DataFrame(selected_data)
        df_branches = df_branches[df_branches.index.isin(df_selected.index)]
        selected_points = df_branches.index.tolist()
    else:
        selected_points = []

    fig = go.Figure(data=go.Parcoords(
        dimensions=list([
            dict(range=[0, 1],
                 constraintrange=[0.2, 0.8],
                 label=col,
                 values=df_branches_selected[col]) for col in df_branches_selected.columns
        ]),
        customdata=df_branches_selected.index,
        uirevision=ui_revision
    ))

    fig.layout.plot_bgcolor = 'white'
    fig.layout.paper_bgcolor = 'white'

    return fig
