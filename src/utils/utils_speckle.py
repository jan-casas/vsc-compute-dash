import logging
from typing import List, Tuple, Dict, Optional

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
def initialize_client(host: str = 'https://app.speckle.systems/') -> SpeckleClient or None:
    """
    Initialize the client.

    Args:
        host (str, optional): The host URL. Defaults to 'https://speckle.xyz/'.

    Returns:
        SpeckleClient: A Speckle client.
    """
    try:
        client = SpeckleClient(host)
        account = get_default_account()
        client.authenticate_with_account(account)
        return client

    except Exception as e:
        logging.exception(f"Error initializing Speckle client: {e}")
        return None


client: SpeckleClient = initialize_client()
transport = ServerTransport(client=client, stream_id=project_id)


# Get data associated to the model
def model_metadata() -> Tuple[str, List[str]]:
    """
    Get the names of the branches of a stream.

    Returns:
        Tuple[str, List[str]]: A tuple containing the initial branch and a list of branch names.
    """
    try:
        models = client.branch.list(project_id)
        models_names = [model.name for model in models]
        initial_model = models_names[0] if models_names else None
        return initial_model, models_names

    except Exception as e:
        logging.exception(f"No models found in project '{project_id}': {e}")
        return "", []


default_model, models_names = model_metadata()
compute_models_names = [name for name in models_names if name.startswith('compute/')]


def model_data(names_models: List[str], selected_commits: Optional[List[str]] = None):
    """
    Returns the latest commit, all commit data, the latest commit object, and an authenticated
    server transport.

    Args:
        names_models: The names of the models.
        selected_commits: The selected commits.
    Returns:
        Tuple[Base, List[Dict[str, Any]], Base, ServerTransport]: A tuple containing the latest
        commit
        object, a list of all commit data, the latest commit object, and an authenticated server
        transport.
    """
    models = client.branch.list(project_id)

    # Filter the selected models
    if selected_commits:
        names_models.append('compute/facade')
    filter_model = [b for b in models if b.name in names_models]
    # for model in names_models:
    #     filter_model += [b for b in models if b.name == model]
    selected_models_ids = [b.id for b in filter_model]

    # Get the commits of the selected models
    commits = [model.commits.items for model in filter_model]

    if not commits:
        raise ValueError(f"No commits found for branch '{names_models}' in stream '{model_id}'")

    # Commits metadata for the commits
    model_commit_metadata = [
        {k: v for k, v in c.__dict__.items() if k != 'authorAvatar'}
        for commit in commits for c in commit
    ]

    # Get the latest commit
    latest_commits = [commit[0].id for commit in commits]

    # Delete the latest item from the list (compute/facade) and add the selected commits
    if selected_commits:
        latest_commits.pop()
        latest_commits.extend([selected_commits])

    return names_models, selected_models_ids, model_commit_metadata, latest_commits


# Data related to commits (this comes from compute)
def commits_metadata(commits: list) -> list[dict]:
    """
    Processes commits, retrieves commit information, and filters based on provided keys.

    Args:
        commits (List[Base]): A list of commit objects.

    Returns:
        Dict[int, List[str]]: A dictionary of filtered commit information keys.
    """
    try:
        # Capture only the metadata attributes of the commit
        commit_attributes = [{'authorName': commit['authorName'], 'commitId': commit['id'],
                              'message': commit['message'], 'createdAt': commit['createdAt']} for
                             commit in commits]
        return commit_attributes

    except Exception as e:
        logging.exception(e)
        return []


def extract_metadata(commit_id, base_obj, field: str = 'metadata'):
    # Extract individual data from each piece
    brep_values = []
    if isinstance(base_obj, Base):
        for key, value in base_obj.__dict__.items():
            if key.startswith('@') and isinstance(value, list):
                for item in value:
                    if isinstance(item, Base):
                        brep_values.append(item[field].__dict__)
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
            # Aggregate the metadata
            avg_commit_values = aggregate_extracted_metadata(commit_values).to_dict()
            if avg_commit_values:
                commits_attributes[i] = avg_commit_values

        except Exception as e:
            logging.exception(f'Error in commit_info for commit {commit} {e}')
            continue

    return commits_attributes


def commit_data_quantities(selected_commit: str):
    if selected_commit:
        try:
            # Get the commit data
            models = client.branch.list(project_id)
            filter_model = next((b for b in models if b.name == 'compute/facade'), None)
            if not filter_model:
                raise ValueError(f"No model found with name 'compute/facade'")

            commits = filter_model.commits.items
            filtered_commit = next((commit for commit in commits if commit.id == selected_commit),
                                   None)
            if not filtered_commit:
                raise ValueError(f"No commit found with id '{selected_commit}'")

            # Get the metadata of the referenced object
            collection_data = operations.receive(filtered_commit.referencedObject, transport)
            commit_values = extract_metadata(selected_commit, collection_data.Data,
                                             'metadata')
            return commit_values

        except Exception as e:
            raise ValueError(f"Error in commit_info for commit {selected_commit}")


# Operations related with commits
def update_commit(names_models):
    """
    Updates the branch commits.
    """
    try:
        # Get commits from the models
        names_models, _, model_commit_metadata, _ = model_data(names_models)
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

    except Exception as e:
        logging.exception(e)
        return pd.DataFrame(), pd.DataFrame()


def merge_commits(selected_models: List[str], selected_commits: Optional[List[str]] = None) -> str:
    """
    Merge the base commit and the selected commits into a single dataframe.

    Args:
        selected_models (Optional[List[str]], optional): The selected commits. Defaults to None.
        selected_commits (Optional[List[str]], optional): The selected commits. Defaults to None.
    Returns:
        str: The url of the iframe.
    """
    try:
        # Get latest commits from the stream and the base one
        names_models, selected_models_ids, selected_commits_ids, latest_commits_ids = model_data(
            selected_models,
            selected_commits)

        base_commit_url = f"{SPECKLE_HOST}/projects/{SPECKLE_PROJECT}/models"
        iframe_style = f"#embed=%7B%22isEnabled%22%3Atrue%2C%22isTransparent%22%3Atrue%7D"
        embed_url = ','.join(
            [f"{name}@{model_id}" for name, model_id in
             zip(selected_models_ids, latest_commits_ids)]
        )
        embed_url = f"{base_commit_url}/{embed_url}/{iframe_style}"

        """
        https://app.speckle.systems/projects/013613abb4/
        models/df7967e0d3@32fd4ff096,e1abc29f0c@a70a8826d4
        modelId1@version, modelId2@version
        """
        return embed_url

    except Exception as e:
        logging.exception(e)
        return ""
