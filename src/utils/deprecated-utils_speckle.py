import logging
import time
from typing import List, Tuple, Dict

from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.transports.server import ServerTransport

speckle_logger = logging.getLogger('specklepy')
speckle_logger.setLevel(logging.CRITICAL)


def get_commits(stream_id: str, client, limit: int = 10, name_branch: str = 'main'):
    """
    Returns the latest commit, all commit data, the latest commit object, and an authenticated
    server transport.

    Args:
            stream_id (str): The ID of the stream.
            host (str, optional): The host URL. Defaults to 'https://speckle.xyz/'.

    Returns:
            Tuple[Base, List[Dict], Base, ServerTransport]: A tuple containing the latest commit
            object,
            a list of all commit data,
            the latest commit object, and an authenticated server transport.
    """
    # Filter by branch name. Get all commits from the stream
    branches = client.branch.list(stream_id)
    commits = []
    for branch in branches:
        if branch.__dict__['name'] == name_branch:
            commits = branch.__dict__['commits'].__dict__['items']
            break
    latest_commit = commits[0]

    # create a df with the dict_latest_commit and values of the commit and remove 'authorAvatar'
    dict_latest_commit = latest_commit.__dict__
    dict_latest_commit.pop('authorAvatar')

    # Commit data
    commit_data = []
    for commit in commits:
        dict_latest_commit = commit.__dict__
        if 'authorAvatar' in dict_latest_commit:
            dict_latest_commit.pop('authorAvatar')
        commit_data.append(dict_latest_commit)

    # create an authenticated server transport from the client and receive the commit obj
    transport = ServerTransport(client=client, stream_id=stream_id)
    obj_id = latest_commit.referencedObject

    res = operations.receive(obj_id, transport)

    return latest_commit, commits, commit_data, transport


def access_branch_objects(tree_objects: Base) -> List[Base]:
    """
    Extracts branch objects from a tree object.

    Args:
        tree_objects (Base): A tree object.

    Returns:
        List[Base]: A list of branch objects.
    """
    return tree_objects['@{0}']


def access_commit_data(loop_commit: Base, transport: ServerTransport, limit: int = 20) -> Dict:
    """
    Accesses commit data and returns a dictionary of attributes.

    Args:
        loop_commit (Base): A commit object.
        transport (ServerTransport): An authenticated server transport.
        limit (int, optional): The maximum number of objects to return. Defaults to 20.

    Returns:
        Dict: A dictionary of attributes.
    """
    try:
        # get obj id from commit
        obj_id = loop_commit.referencedObject
        # receive objects from commit
        commit_data = operations.receive(obj_id, transport)

        tree = commit_data.__dict__['@Data']['id']
        tree_objects = operations.receive(tree, transport)

        branch_objects = access_branch_objects(tree_objects)
        branch_objects_limit = branch_objects[:limit]

        dict_attributes_plot: Dict = {}
        for i, b in enumerate(branch_objects_limit):
            # add items attributes
            dict_attributes_plot[i] = {}
            keys_object = b.get_serializable_attributes()
            keys_object.remove('@obj')
            for k in keys_object:
                if k.startswith('@'):
                    dict_attributes_plot[i][k] = b[k]

            # add commit values
            dict_attributes_plot[i].update({
                "authorName": loop_commit.authorName,
                "commitId": loop_commit.id,
                "message": loop_commit.message,
                "totalChildrenCount": loop_commit.totalChildrenCount
            })

        return dict_attributes_plot
    except Exception as e:
        logging.exception(f'Error in access_commit_data in {loop_commit.id}')
        return None


def process_commit(commit, transport) -> Dict:
    """
    Processes commits sequentially and returns a dictionary of attributes.

    Args:
        commit (Base): A commit object.
        transport (ServerTransport): An authenticated server transport.

    Returns:
        Dict: A dictionary of attributes.
    """
    try:
        start = time.time()
        result = access_commit_data(commit, transport)
        end = time.time()
        print("Time: ", end - start)
        return result
    except Exception as e:
        pass


def process_commits(commits, transport) -> Dict:
    """
    Processes commits in parallel and returns a dictionary of attributes.

    Args:
        commits (List[Base]): A list of commit objects.
        transport (ServerTransport): An authenticated server transport.

    Returns:
        Dict: A dictionary of attributes.
    """
    dict_attributes = {}
    start = time.time()
    for i, commit in enumerate(commits):
        result = process_commit(commit, transport)
        if result is not None:
            dict_attributes[i] = result
    end = time.time()
    logging.info(f'Processed {len(dict_attributes)} commits in {end - start} seconds.')
    return dict_attributes


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


def get_branch_names(client, stream_id='0e5d383e76') -> Tuple[str, List[str]]:
    """
    Get the names of the branches of a stream.

    Args:
        client (SpeckleClient): A Speckle client.
        stream_id (str, optional): The ID of the stream. Defaults to '0e5d383e76'.

    Returns:
        Tuple[str, List[str]]: A tuple containing the initial branch and a list of branch names.
    """
    branches = client.branch.list(stream_id)
    branch_names = [branch.name for branch in branches]
    initial_branch = branch_names[0]

    return initial_branch, branch_names


client = initialize_client()
initial_branch, branch_names = get_branch_names(client)

# TODO: ojo que solo está cogiendo el valor de la primera fila de cada comit, no los 130... (
#  debería hacer
#  agregaciones sobre esto)
