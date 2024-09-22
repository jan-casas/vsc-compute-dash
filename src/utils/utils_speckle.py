import logging
import time
from typing import List, Tuple, Dict, Any

import pandas as pd
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.transports.server import ServerTransport

from config.settings import SPECKLE_MODEL_ID, SPECKLE_HOST, SPECKLE_PROJECT

project_id = SPECKLE_PROJECT
model_id: str = SPECKLE_MODEL_ID  # TODO: Make this selectable
store_commits_names: list = []
store_dict_attributes: dict = {}


# Initialize Speckle clients and obtain initial data
def initialize_client(host: str = 'https://app.speckle.systems/') -> SpeckleClient:
    """
    Initialize the client.

    Args:
        host (str, optional): The host URL. Defaults to 'https://speckle.xyz/'.

    Returns:
        SpeckleClient: A Speckle client.
    """
    client = SpeckleClient(host)
    account = get_default_account()
    client.authenticate_with_account(account)
    return client


client: SpeckleClient = initialize_client()
transport = ServerTransport(client=client, stream_id=project_id)


# Get data associated to the model
def model_metadata() -> Tuple[str, List[str]]:
    """
    Get the names of the branches of a stream.

    Args:
        client (SpeckleClient): A Speckle client.
        project_id (str, optional): The ID of the stream. Defaults to '0e5d383e76'.

    Returns:
        Tuple[str, List[str]]: A tuple containing the initial branch and a list of branch names.
    """
    models = client.branch.list(project_id)
    models_names = [model.name for model in models]
    initial_model = models_names[0] if models_names else None
    return initial_model, models_names


default_model, models_names = model_metadata()


def model_data(names_models: List[str]):
    """
    Returns the latest commit, all commit data, the latest commit object, and an authenticated
    server transport.

    Args:
        project_id:
        names_models:
        client (SpeckleClient): A Speckle client.
        model_id (str): The ID of the stream.
        names_models (str, optional): The name of the branch. Defaults to 'main'.

    Returns:
        Tuple[Base, List[Dict[str, Any]], Base, ServerTransport]: A tuple containing the latest
        commit
        object, a list of all commit data, the latest commit object, and an authenticated server
        transport.
    """
    branches = client.branch.list(project_id)
    filter_branches = list(b for b in branches if b.name == names_models)
    selected_model = [b.id for b in filter_branches]

    commits = []
    for branch in filter_branches:
        commits = branch.commits.items
        break

    if not commits:
        raise ValueError(f"No commits found for branch '{names_models}' in stream '{model_id}'")

    latest_commit_per_model = commits[-1]

    model_commit_metadata = []
    for commit in commits:
        commit_dict = commit.__dict__
        commit_dict.pop('authorAvatar', None)
        model_commit_metadata.append(commit_dict)

    return names_models, selected_model, latest_commit_per_model, model_commit_metadata


# Data related to commits (this comes from compute)
def commits_metadata(commits: list) -> list[dict]:
    """
    Processes commits, retrieves commit information, and filters based on provided keys.

    Args:
        client (SpeckleClient): A Speckle client.
        project_id (str): The ID of the stream.
        commits (List[Base]): A list of commit objects.

    Returns:
        Dict[int, List[str]]: A dictionary of filtered commit information keys.
    """
    try:
        # Capture only the metadata attributes of the commit
        commit_attributes = [{'authorName': commit['authorName'], 'commitId': commit['id'],
                              'message': commit['message']} for commit in commits]
        return commit_attributes
    except Exception as e:
        logging.exception(e)
        return []


def extract_metadata(commit_id, base_obj):
    # Extract individual data from each piece
    brep_values = []
    if isinstance(base_obj, Base):
        for key, value in base_obj.__dict__.items():
            if key.startswith('@') and isinstance(value, list):
                for item in value:
                    if isinstance(item, Base):
                        brep_values.append(item.metadata.__dict__)
                        brep_values[-1]['commitId'] = commit_id

    return brep_values


def aggregate_extracted_metadata(brep_values):
    # If you want to evaluate the overall commit data you should use aggregations
    df = pd.DataFrame(brep_values)
    metadata_commit_values = df.agg(
        lambda x: round(x.mean(), 2) if pd.api.types.is_numeric_dtype(x) else x.iloc[0])
    return metadata_commit_values


def commits_data(commits: list) -> dict:
    """
    Processes commits, retrieves commit information, and filters based on provided keys.

    Args:
        client (SpeckleClient): A Speckle client.
        project_id (str): The ID of the stream.
        commits (List[Base]): A list of commit objects.

    Returns:
        Dict[int, List[str]]: A dictionary of filtered commit information keys.
    """
    commits_attributes = {}
    for i, commit in enumerate(commits):
        try:
            # Get the metadata of the referenced object
            collection_data = operations.receive(commit['referencedObject'], transport)
            commit_values = extract_metadata(commit['id'], collection_data.Data)
            avg_commit_values = aggregate_extracted_metadata(commit_values).to_dict()
            if avg_commit_values:
                commits_attributes[i] = avg_commit_values

        except Exception as e:
            logging.exception(f'Error in commit_info for commit {commit} {e}')
            continue

    return commits_attributes


# Operations related with commits
def update_commit(names_models):
    """
    Updates the branch commits.
    """
    # Get commits from the models
    names_models, _, _, model_commit_metadata = model_data(names_models)
    new_commits: list = [commit for commit in model_commit_metadata if commit['id'] not in
                         store_commits_names]

    # Capture only the attributes of the objects baked in Compute
    filter_commit_metadata = commits_metadata(model_commit_metadata)
    store_commits_names.extend(commit['commitId'] for commit in filter_commit_metadata)
    selected_commit_metadata: pd.DataFrame = pd.DataFrame(filter_commit_metadata)

    # FIXME: Dale una vuelta a esto, es correcta la condición?
    if not new_commits and store_commits_names:
        selected_commit_data = pd.DataFrame.from_dict(store_dict_attributes).T
        return selected_commit_metadata, selected_commit_data

    commit_attributes = commits_data(model_commit_metadata)
    store_dict_attributes.update(commit_attributes)

    # Construct the df used in the parallel plot
    selected_commit_data = pd.DataFrame.from_dict(store_dict_attributes).T

    return selected_commit_metadata, selected_commit_data


def merge_commits(selected_models: List[str]) -> str:
    """
    Merge the base commit and the selected commits into a single dataframe.

    Args:
        selected_models (Optional[List[str]], optional): The selected commits. Defaults to None.

    Returns:
        str: The url of the iframe.
    """
    # Get latest commits from the stream and the base one
    names_branch, filter_branches_names, latest_commit, _ = model_data(selected_models)
    base_commit_url = f"{SPECKLE_HOST}/projects/{SPECKLE_PROJECT}/models"
    embed_url = ','.join(filter_branches_names)
    embed_url = (f"{base_commit_url}/"
                 f"{embed_url}#embed=%7B%22isEnabled%22%3Atrue%2C%22isTransparent%22%3Atrue%7D")

    return embed_url
