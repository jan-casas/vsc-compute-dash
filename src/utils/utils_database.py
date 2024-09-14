'''
Connect to a Postgres database and retrieve the data from the IFCROOT table.
https://speckle.guide/dev/apps.html
https://speckle.community/t/version-diffing-with-python-part-1/5614
https://github.com/izzylys/demo-specklepy
https://speckle.systems/tutorials/scheduling-app-for-revit-data/
https://speckle.guide/dev/py-sample.html
https://speckle.guide/dev/server-rest-api.html
https://speckle.community/t/serializing-objects-with-multiple-relations/2013
'''


import sqlite3

import psycopg2
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from specklepy.transports.server import ServerTransport

# Mapping parameter
# class Concrete(Base):
#     density: str = 2400
#     embodied_carbon = 0.159

MATERIALS_MAPPING = {
    "IfcRoot_Description": "Concrete",
}


def read_postgres_table():
    # Connect to the database
    connection = psycopg2.connect(
        user="postgres", password=PASSWORD, host="localhost", port="5432", database="postgres"
    )
    cursor = connection.cursor()

    # Read table
    cursor.execute("SELECT * FROM public.ifcroot;")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    # Close connection
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

    return record


def read_sqlite_table():
    # Connect to the database
    connection = sqlite3.connect("C:/Users/alexa/OneDrive/Documents/GitHub/thesis/thesis/data/ifc/IFC4_ADD2_TC1.exp")
    cursor = connection.cursor()

    # Read table
    cursor.execute("SELECT * FROM public.ifcroot;")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

    # Close connection
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")

    return record


def initialise_speckle(HOST, STREAM_ID, COMMIT_ID):
    HOST = 'https://speckle.xyz/'
    STREAM_ID = '2283252f56'
    COMMIT_ID = 'f0c93d841f'

    # create and authenticate a client
    client = SpeckleClient(host=HOST)
    account = get_default_account()
    client.authenticate_with_account(account)

    # get the specified commit data
    commit = client.commit.get(STREAM_ID, COMMIT_ID)

    # create an authenticated server transport from the client and receive the commit obj
    transport = ServerTransport(client=client, stream_id=STREAM_ID)
    obj_id = commit.referencedObject

    res = operations.receive(obj_id, transport)

    return print("- Commit: ", commit, "\n- Object id: ", transport, "\n- Commit data: ", res)


def navigate_tree():
    tree = commit_data.__dict__['elements'][0]['id']
    tree_objects = operations.receive(tree, transport)
    branch = tree_objects.__dict__["elements"][6]["id"]
    branch_objects = operations.receive(branch, transport)
    items = [branch_objects.__dict__["elements"][i]["id"] for i in range(len(branch_objects.__dict__["elements"]))]
    items_objects = [operations.receive(item, transport) for item in items]

    return items_objects


def add_parameter_data(level: Base) -> Base:
    # Retrieve the names of all members (properties, lists) from the level object
    names = level.get_member_names()
    name = 'IfcRoot_Description'
    # for name in names:
    #     try:
    print(name)
    if name not in MATERIALS_MAPPING.keys():
        print(f"Property with name '{name}' is not found in MATERIALS_MAPPING dictionary")
        pass
        # break # If property with specified name is not found, skip it
    # If property with specified name is found, get registered type which corresponds to the material key in MATERIALS_MAPPING dictionary
    # material = Base.get_registered_type(MATERIALS_MAPPING[name])()
    material = MATERIALS_MAPPING[name]
    print(material)
    # Then assign the retrieved material value to the '@material' key of the property or each item in a list with specified name
    # prop = level[name]
    # prop = level.__dict__[name]
    # prop = level['userStrings'].__dict__[name]
    prop = level['userStrings']
    print(prop)
    if isinstance(prop, Base):
        prop[name] = material
    elif isinstance(prop, list):
        for item in prop:
            item[name] = material
        # except Exception as e:
        #     print(f"Error occurred while assigning material to property '{name}': {e}")
        #     pass
    return level


def send_with_parameters(branch_name, description, message):
    # add the materials data to our levels
    levels = [add_materials_data(level) for level in items_objects]
    # print(levels)
    # create a base object to hold the list of levels
    base = Base(data=levels)
    # print(levels[0].__dict__)

    # create a branch if you'd like
    # branch_name = "🐍 demo_CONCRETEffds"
    branches = client.branch.list(STREAM_ID)
    has_res_branch = any(b.name == branch_name for b in branches)
    if not has_res_branch:
        client.branch.create(
            STREAM_ID, name=branch_name, description=description
        )

    # create a base object to hold the list of levels
    base = Base(data=levels)
    # and send the data to the server and get back the hash of the object
    obj_id = operations.send(base, [transport])

    # now create a commit on that branch with your updated data!
    commid_id = client.commit.create(
        STREAM_ID,
        obj_id,
        branch_name,
        message=message,
    )

    return print("Commit id: ", commid_id)


if __name__ == "__main__":
    initialise(HOST, STREAM_ID, COMMIT_ID)
    navigate_tree()
    send_with_parameters(branch_name='🙌 done!', description="new stuff from py", message="add detached material")
