import logging
import time
from typing import List, Tuple, Dict, Any

from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.transports.server import ServerTransport

from config.settings import SPECKLE_MODEL_ID, SPECKLE_HOST, SPECKLE_PROJECT

model_id = SPECKLE_MODEL_ID


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


def model_data(client: SpeckleClient, project_id: str) -> Tuple[str, List[str]]:
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


def commits_data(client: SpeckleClient, project_id, model_id: str, names_branch: List[str]):
    """
    Returns the latest commit, all commit data, the latest commit object, and an authenticated
    server transport.

    Args:
        project_id:
        names_branch:
        client (SpeckleClient): A Speckle client.
        model_id (str): The ID of the stream.
        names_branch (str, optional): The name of the branch. Defaults to 'main'.

    Returns:
        Tuple[Base, List[Dict[str, Any]], Base, ServerTransport]: A tuple containing the latest
        commit
        object, a list of all commit data, the latest commit object, and an authenticated server
        transport.
    """
    branches = client.branch.list(project_id)
    filter_branches = list(b for b in branches if b.name in names_branch)
    filter_branches_names = [b.id for b in filter_branches]

    commits = []
    for branch in filter_branches:
        commits = branch.commits.items
        break

    if not commits:
        raise ValueError(f"No commits found for branch '{names_branch}' in stream '{model_id}'")

    latest_commit = commits[-1]

    commit_data = []
    for commit in commits:
        commit_dict = commit.__dict__
        commit_dict.pop('authorAvatar', None)
        commit_data.append(commit_dict)

    return names_branch, filter_branches_names, latest_commit, commit_data


def commit_info_available(commit: Dict[str, Any]) -> List[str]:
    """
    Get available commit information keys.

    Args:
        commit (Dict[str, Any]): A commit dictionary.

    Returns:
        List[str]: A list of available commit information keys.
    """
    return list(commit.keys())


# TODO: REVISA ESTA FUNCIÓN
def process_commits(client: SpeckleClient, branch_id: str, commits: List[Base],
                    info_keys: List[str] = None) -> Dict[int, List[str]]:
    """
    Processes commits, retrieves commit information, and filters based on provided keys.

    Args:
        client (SpeckleClient): A Speckle client.
        branch_id (str): The ID of the stream.
        commits (List[Base]): A list of commit objects.
        info_keys (List[str]): A list of keys to filter.

    Returns:
        Dict[int, List[str]]: A dictionary of filtered commit information keys.
    """
    dict_attributes = {}
    start = time.time()
    for i, commit in enumerate(commits):
        try:
            transport = ServerTransport(client=client, stream_id=branch_id)
            obj_id = commit['referencedObject']
            collection_data = operations.receive(obj_id, transport)
            elements = collection_data.elements

            for element in elements:
                element_id = element['id']
                operations.receive(element_id, transport)

            object_info = elements[0].elements[0].__dict__.keys()
        except Exception as e:
            logging.exception(f'Error in commit_info for commit {commit.id}: {e}')
            object_info = None

        if object_info is not None:
            available_keys = list(object_info)
            logging.info(f'Available commit info: {available_keys}')
            filtered_info = [key for key in available_keys if key in info_keys]
            dict_attributes[i] = filtered_info

    end = time.time()
    logging.info(f'Processed {len(dict_attributes)} commits in {end - start} seconds.')
    return dict_attributes


def object_info(client: SpeckleClient, model_id: str, obj_id: str) -> Base:
    """
    Retrieve object information.

    Args:
        client (SpeckleClient): A Speckle client.
        model_id (str): The ID of the stream.
        obj_id (str): The ID of the object.

    Returns:
        Base: The object data.
    """
    transport = ServerTransport(client=client, stream_id=model_id)
    return operations.receive(obj_id, transport)


def merge_commits(client, model_id, selected_models: List[str]) -> str:
    """
    Merge the base commit and the selected commits into a single dataframe.

    Args:
        selected_models (Optional[List[str]], optional): The selected commits. Defaults to None.

    Returns:
        str: The url of the iframe.
    """
    # Get latest commits from the stream and the base one
    names_branch, filter_branches_names, latest_commit, _ = commits_data(client, SPECKLE_PROJECT,
                                                                         model_id,
                                                                         selected_models)
    base_commit_url = f"{SPECKLE_HOST}/projects/{SPECKLE_PROJECT}/models"
    embed_url = ','.join(filter_branches_names)
    embed_url = f"{base_commit_url}/{embed_url}"

    return embed_url


# Initialize Speckle clients and obtain initial data
client = initialize_client()
default_model, models_names = model_data(client, SPECKLE_PROJECT)
