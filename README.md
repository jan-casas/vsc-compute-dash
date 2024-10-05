# Compute Version Control

## Overview

Compute Version Control (VSC) aims to provide a comprehensive version control system that validates
design proposals based on design and constructive system constraints. These constraints are provided
by manufacturers and return essential information about the lifecycle of materials and associated
data. The solution is designed to streamline project management and enhance decision-making by
ensuring designs meet both technical and regulatory requirements.

## Benefits and Business Intelligence

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

## System Components

The application consists of three primary components:

1. **Rhino Compute**: Handles predefined manufactured systems. It generates constructive solutions,
   such as creating glass facades from provided input surfaces.
2. **Speckle**: A data repository model that provides storage for baked geometry. Speckle is
   particularly useful for managing geometry IDs, variations, and provides tools for filtering and
   differentiation.
3. **PostgreSQL Database**: Associates geometry IDs with lifecycle data, providing efficient data
   tracking and retrieval.

This project delivers a robust solution for managing and validating design proposals, enhancing
accuracy and efficiency by leveraging manufacturer-provided constraints.

## Architecture Overview

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

### Components Explained:

- `RHINO_COMPUTE`: Represents the component responsible for generating geometry.
- `GEOMETRY`: Represents the output geometry from Rhino Compute.
- `SPECKLE`: Stores and manages the created geometry.
- `GEOMETRY_ID`: The unique ID of each piece of geometry managed by Speckle.
- `POSTGRESQL_DATABASE`: Associates geometry with lifecycle data.
- `MATERIAL_LIFECYCLE_DATA`: Represents the lifecycle information of each material.

## Table of Contents

- [Project Structure](#project-structure): Organization of the project, including main files,
  languages, and frameworks.
- [Speckle Structure](#speckle-structure): Details of the Speckle data repository for managing
  geometry.
- [Database Structure](#database-structure): Explanation of the database's role in managing
  construction project data.

## Project Structure

The project is composed of two Docker containers: one for the Node.js project (Rhino Compute server)
and one for the Python project (Dash application). Both containers communicate within the same
network.

- **Node.js Project**: Rhino Compute server, responsible for generating geometry data.
- **Python Project**: Dash application that interacts with the Node.js project, providing a user
  interface for visualization.

```plaintext
vsc-compute-dash
├── files
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

## Languages and Frameworks

- **Python**: Main programming language used.
- **Flask**: Web framework to create application endpoints.
- **psycopg2**: PostgreSQL adapter for Python.
- **Dash**: Framework for building analytical web applications.
- **Docker**: Containerization platform for deployment.
- **PostgreSQL**: Relational database management system.
- **Speckle**: Data repository for baked geometry.

## Speckle Structure

Speckle provides storage for all baked geometry and is useful for managing geometry IDs and their
variations. The Speckle iframe is used to display geometry and its variations in the Python project,
with the Python container connected to the Speckle server.

### Speckle Components:

- **Geometry**: Created by Grasshopper and Rhino Compute.
- **System Parts**: Components associated with the geometry.
- **Part Data**: Data linked with each system part.
- **Metadata**: Additional data about geometry.

Further Steps:

- Deploy Speckle in a separate container (Windows VM).
- Update the IP address of `compute.rhino3d.appserver` to match that of the Flask application.
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

## Database Structure

This project uses SQLite3 (local) and PostgreSQL as the primary database systems to store and manage
construction project data.

### Key Roles:

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
- **Storing Construction Project Data**: Manages construction project details, including ownership,
  timelines, and associated constructive systems.

```mermaid
erDiagram
    USER {
        int id
        string name
    }
    PARAMETER_VARIATION {
        int id
        string parameter_name
        string value
        int user_id
    }
    MATERIAL {
        int id
        string name
        string type
    }
    PROCESS {
        int id
        string name
        string description
    }
    MANUFACTURER {
        int id
        string name
        string location
    }
    CONSTRUCTION_PROJECT {
        int id
        string name
        date start_date
        date end_date
        int user_id
        int constructive_system_id
    }
    TIME_TRACKING {
        int id
        date start_time
        date end_time
        string phase
    }
    MATERIAL_METADATA {
        int id
        string property
        string value
    }
    ENVIRONMENTAL_CONDITION {
        int id
        string condition
        string value
    }
    CONSTRUCTIVE_SYSTEM {
        int id
        string name
        string description
    }
    MATERIAL_USAGE {
        int id
        string part
    }
    USER ||--|| CONSTRUCTIVE_SYSTEM: "REQUESTS"
    USER ||--|| PARAMETER_VARIATION: "MAKES"
    USER ||--|| CONSTRUCTION_PROJECT: "OWNS"
    CONSTRUCTIVE_SYSTEM ||--|| PARAMETER_VARIATION: "HAS"
    CONSTRUCTIVE_SYSTEM ||--|| CONSTRUCTION_PROJECT: "USED_IN"
    MATERIAL ||--|| PROCESS: "HAS"
    MATERIAL ||--|| MANUFACTURER: "PRODUCED_BY"
    MATERIAL ||--|| MATERIAL_METADATA: "HAS"
    MATERIAL ||--|| MATERIAL_USAGE: "USED_IN"
    PROCESS ||--|| TIME_TRACKING: "HAS"
    PROCESS ||--|| ENVIRONMENTAL_CONDITION: "HAS"
    CONSTRUCTIVE_SYSTEM ||--|| MATERIAL_USAGE: "USES"
```

In this diagram:

- `MATERIAL` represents the materials used in construction, such as wood, concrete, and steel. Each
  material has a
  unique ID, a name, and a type.

- `PROCESS` represents the processes involved in the lifecycle of the materials, such as processing,
  manufacturing, and
  construction. Each process has a unique ID, a name, and a description.

- `MANUFACTURER` represents the manufacturers that produce the materials. Each manufacturer has a
  unique ID, a name, and
  a location.

- `CONSTRUCTION_PROJECT` represents the construction projects that use the materials. Each project
  has a unique ID, a
  name, and start and end dates.

The relationships between the entities are as follows:

- Each `MATERIAL` has one or more `PROCESS`es.
- Each `MATERIAL` is produced by one `MANUFACTURER`.
- Each `MATERIAL` is used in one or more `CONSTRUCTION_PROJECT`s.

## Conclusion

Compute Version Control offers a powerful solution for managing and validating design proposals,
enhancing the efficiency and accuracy of the design process. By leveraging the combined capabilities
of Rhino Compute, Speckle, and PostgreSQL, the system provides a comprehensive approach to version
control and lifecycle management in construction projects.

For more information, refer to the documentation or contact the project maintainers.
