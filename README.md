# Unlocking Business Intelligence through Compute Version Control

_In the Architecture, Engineering, and Construction (AEC) sector, there is a lack of flexibility
present in disciplines such as software development, where specific libraries can be easily imported
and used.
This project aims to develop a tool that allows architects and computational designers to quickly
test
manufacturers' constructive solutions. Additionally, manufacturers will be able to obtain
information about the use of their products and customer needs._

[//]: # (<video width="100%" controls>)

[//]: # (  <source src="src/static/assets/compute_vsc.mp4" type="video/mp4">)

[//]: # (  Your browser does not support the video tag.)

[//]: # (</video>)

![Compute Version Control](src/static/assets/readme.png)

### Table of Contents

- [Overview](#overview): Summary of the project's objectives and benefits.
- [Benefits and Business Intelligence](#benefits-and-business-intelligence): Explanation of the
  benefits and business intelligence insights provided by the system.
- [Architecture Approach](#architecture-approach): Overview of the system's architecture and
  components.
- [Project Structure](#project-structure): Organization of the project, including main files,
  languages, and frameworks.
- [Rhino Compute](#rhino-compute): Explanation of the Rhino Compute service and its role in
  generating geometry data.
- [Speckle Systems](#speckle-systems): Explanation of the Speckle system and its role in managing
  geometry data.
- [Database Configuration](#database-configuration): Details on the database configuration and its
  role in storing and managing construction project data.
- [Conclusion](#conclusion): Summary of the project's objectives and benefits.

## Overview

`Compute Version Control` (VSC) aims to provide a comprehensive version control system that
validates
design proposals based on design and constructive system constraints. These constraints are provided
by manufacturers and return essential information about key indicators such as cost, material,
geometrical constraints, and lifecycle data.

### Benefits and Business Intelligence

This system offers several benefits and unlocks numerous possibilities from a business intelligence
perspective:

- **Enhanced Decision-Making**: Detailed insights into the lifecycle of materials and their
  associated data allow businesses to make informed decisions regarding material selection and
  project planning.
- **Cost Efficiency**: Identifying cost-effective materials and construction processes can lead to
  significant cost savings.
- **Improved Compliance**: Ensures that all design proposals adhere to manufacturer-provided
  constraints, improving compliance with industry standards and regulations.
- **Data-Driven Insights**: Integration with PostgreSQL and Speckle provides robust data management
  and retrieval, enabling businesses to gain valuable insights into project performance and material
  usage.
- **Streamlined Workflow**: Automates validation and management of design proposals, reducing manual
  effort and increasing efficiency.
- **Scalability**: The modular architecture allows for easy scalability to accommodate growing
  business needs.

### Architecture Approach

The application consists of three primary components:

1. **Rhino Compute**: Handles predefined manufactured systems. It generates constructive solutions,
   such as creating glass facades from provided input surfaces.
2. **Speckle**: A data repository model that provides storage for baked geometry. Speckle is
   particularly useful for managing geometry IDs, variations, and provides tools for filtering and
   differentiation.
3. **Database**: Associates geometry IDs with lifecycle data, providing efficient data
   tracking and retrieval.

This project delivers a robust solution for managing and validating design proposals, enhancing
accuracy and efficiency by leveraging manufacturer-provided constraints.

```mermaid
graph LR
    SPECKLE_CLIENT -->|retrieves| INPUT_GEOMETRY
    INPUT_GEOMETRY -->|processed by| RHINO_COMPUTE
    RHINO_COMPUTE -->|creates| GEOMETRY
    GEOMETRY -->|stores| SPECKLE
    SPECKLE -->|manages| GEOMETRY_ID
    GEOMETRY_ID -->|associates| POSTGRESQL_DATABASE
    MATERIAL_LIFECYCLE_DATA -->|associates| POSTGRESQL_DATABASE
    POSTGRESQL_DATABASE -->|updates| SPECKLE
    SPECKLE -->|updates| SPECKLE_CLIENT
```

In this diagram:

- `RHINO_COMPUTE`: Represents the component responsible for generating geometry.
- `GEOMETRY`: Represents the output geometry from Rhino Compute.
- `SPECKLE`: Stores and manages the created geometry.
- `GEOMETRY_ID`: The unique ID of each piece of geometry managed by Speckle.
- `POSTGRESQL_DATABASE`: Associates geometry with lifecycle data.
- `MATERIAL_LIFECYCLE_DATA`: Represents the lifecycle information of each material.

## Project Structure

The project is composed of two Docker containers: one for the Node.js project (Rhino Compute server)
and one for the Python project (Dash application) https://dash.plotly.com/. Both containers
communicate within the same
network.

- **Node.js Project**: Rhino Compute server, responsible for generating geometry
  data.
- **Python Project**: Dash application that interacts with the Node.js project, providing a user
  interface for visualization.

```plaintext
vsc-compute-dash
└── src
    ├── callbacks
    │   ├── callback_compute.py
    │   ├── callback_speckle.py
    │   └── callback_views.py
    ├── config
    │   ├── logs.py
    │   └── settings.py
    ├── utils
    │   ├── utils.py
    │   └── utils_speckle.py
    ├── views
    │   ├── default_components.py
    │   └── layout_landing.py
    └── __init__.py
    └── core_callbacks.py
├── compute.db
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

In detail:

- `src/callbacks/callback_compute.py`: Defines callbacks and API endpoints for a Dash and Flask app
  to manage slider interactions, update stores, send data to a compute server, and manage SQLite
  database operations.
- `src/callbacks/callback_speckle.py`: Defines callbacks for a Dash app interacting with Speckle
  data, handling user inputs, updating data stores, merging commits, and updating UI components to
  reflect user selections.
- `src/callbacks/callback_views.py`: Defines callbacks for managing the interactive UI elements in a
  Dash app, such as toggling visibility of sidebars and collapsible sections based on user
  interactions.
- `src/utils/utils_speckle.py`: Contains utility functions for interacting with the Speckle API,
  managing construction model data, processing commits, and integrating version control features
  into project workflows.

> [!IMPORTANT]  
> The project is only tested on a local machine and is not yet deployed to a production server.
> The aim is to deploy the project (Speckle Server, Rhino Compute) to a
> Windows VM
> server in the future.

## Main Systems

### Rhino Compute

This service provides a cloud-based, stateless REST API for performing geometry calculations on
various objects like points, curves, surfaces, meshes, and solids. It offers extensive access to
over 2400 RhinoCommon API calls, including unique functions like closest point and intersection
calculations. The solution supports integration with Rhino/Grasshopper plugins and allows
serialization of operations through Grasshopper or Python scripts. Additionally, client libraries
are available for use in standalone applications built in C# (.NET), Python, and
JavaScript.

The script hosted in the appserver repository has unique input and output characteristics. Both use
Speckle components to read and send versions. https://github.com/mcneel/compute.rhino3d.appserver

- Read Component: Retrieves geometry from the Speckle server.
- Manufacturer Geometrical Logic: Generates geometry based on manufacturer constraints.
- Send Component: Sends geometry to the Speckle server.
- Visualize Component: Displays geometry in the appserver.

### Speckle Systems

Speckle provides storage for all baked geometry and is useful for managing geometry IDs and their
variations. The Speckle iframe is used to display geometry and its variations in the Python project,
with the Python container connected to the Speckle server https://speckle.systems/.

- **Geometry**: Created by Grasshopper and Rhino Compute.
- **System Parts**: Components associated with the geometry.
- **Part Data**: Data linked with each system part.
- **Metadata**: Additional data about geometry.

Further Steps:

- Resolve the Speckle read component failure in Grasshopper and add the ability to select branches.

```mermaid
graph LR
    CLIENT_INPUT_GEOMETRY -->|processed by| RHINO_COMPUTE
    CLIENT_INPUT_GEOMETRY -->|stores| SPECKLE
    RHINO_COMPUTE -->|creates| TRANSFORMED_SURFACE
    TRANSFORMED_SURFACE -->|stores| SPECKLE
    SYSTEM_PARTS -->|associates| SPECKLE
    PART_DATA -->|associates| SPECKLE
```

In this diagram:

- `CLIENT_INPUT_GEOMETRY` represents the client's input geometry, such as a surface of a facade.
- `RHINO_COMPUTE` represents the Rhino Compute component that processes the client's input geometry
  and creates the
  transformed surface.
- `TRANSFORMED_SURFACE` represents the new surface created by Rhino Compute.
- `SYSTEM_PARTS` represents the parts of the system that are associated with the transformed
  surface.
- `PART_DATA` represents the data associated with each part of the system.
- `SPECKLE` represents the Speckle component that stores the transformed surface, the system parts,
  and the part data.

### Relational Database

This project uses SQLite3 (local) and PostgreSQL as the primary database systems to store and manage
construction project data and interactions.

- **Storing Geometry Data**: PostgreSQL stores geometry created by Rhino Compute, with each geometry
  piece assigned a unique ID managed by Speckle.
- **Storing Parameter Variations**: Stores variations in parameters for constructive systems,
  tracking user changes.
- **Storing Constructive System Data**: Stores information about constructive systems, allowing
  tracking of their usage in projects.

Further Steps:

- **Associating Geometry with Material Lifecycle Data**: PostgreSQL associates geometry with
  lifecycle data, enabling material tracking throughout the project lifecycle.
- **Storing User Data**: Stores user information, tracking project ownership and parameter
  variations.

> [!NOTE]
> The database structure is currently in development and will be updated in future iterations.
> The current local database is run locally in a SQLite3 file with only one table containing the
> parameters iterations and the commit message.

## Conclusion

Compute Version Control offers a powerful solution for managing and validating design proposals,
enhancing the efficiency and accuracy of the design process. By leveraging the combined capabilities
of Rhino Compute, Speckle, and PostgreSQL, the system provides a comprehensive approach to version
control and lifecycle data on testing iteration project designs. 
