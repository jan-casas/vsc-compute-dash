# Unlocking Business Intelligence for Manufacturers with Compute Version Control

_In the Architecture, Engineering, and Construction (AEC) sector, there is a lack of flexibility
present in disciplines such as software development, where specific libraries can be easily imported
and used.
This project aims to develop a tool that allows architects and computational designers to quickly
test **parametric
manufacturers' constructive solutions, from the web into any of their tools**. Additionally,
manufacturers will be able to **obtain
information** about the use of their products and customer needs._

[//]: # (<video width="100%" controls>)

[//]: # (  <source src="src/static/assets/compute_vsc.mp4" type="video/mp4">)

[//]: # (  Your browser does not support the video tag.)

[//]: # (</video>)

![Compute Version Control](src/static/assets/readme.png)
*Figure 1: Landing page of the Webapp. You can see the Compute and Speckle window and the params
to interact with.*

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

This system offers several benefits and unlocks numerous possibilities from a
`business intelligence`
perspective:

- **Enhanced Decision-Making**: Detailed insights into the lifecycle of materials and their
  associated data allow businesses to make informed decisions regarding material selection and
  project planning.
- **Improved Compliance**: Ensures that all design proposals adhere to manufacturer-provided
  constraints, improving compliance with industry standards and regulations.
- **Data-Driven Insights**: Integration with Relational Databases and Speckle provides robust data
  management
  and retrieval, enabling businesses to gain valuable insights from project interactions.
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
3. **Relational Database**: Associates geometry IDs with lifecycle data, providing efficient data
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

*Diagram 1: General Architecture Proposal to interact with Compute and the clients BI using
Speckle.*

In this diagram:

- `RHINO_COMPUTE`: Represents the component responsible for generating geometry.
- `GEOMETRY`: Represents the output geometry from Rhino Compute.
- `SPECKLE`: Stores and manages the created geometry.
- `GEOMETRY_ID`: The unique ID of each piece of geometry managed by Speckle.
- `POSTGRESQL_DATABASE`: Associates geometry with lifecycle data.
- `MATERIAL_LIFECYCLE_DATA`: Represents the lifecycle information of each material.

## Project Structure

The project is composed of two Docker containers: one for the Node.js project (Rhino Compute server)
and one for the Python project [DASH](https://dash.plotly.com/) web application . Both containers
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
├── building.gh
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
> The aim of this project is developing a minimum viable product (MVP) to test the interaction
> and the link with the Business Intelligence (BI) of the manufacturers.
> Only the [Dolcker & Clip](https://dolcker.es/dolcker-system#descargas) system by Dolcker has been
> implemented.
> The project is only tested on a local machine and is not yet deployed to a production server
> (Speckle Server, Rhino Compute).

### User Interface Overview

The user interface consists of three primary sections: the landing page and two side panels.

- **Landing Page**: Features a split-screen view showcasing the model stored in Speckle alongside
  the model generated by Rhino Compute. Users can adjust parameters to interactively modify the
  model, with updates reflected in real-time.

- **Speckle Optimal Commit Panel**: Displays relevant metadata of the model and allows users to
  filter and select specific commits based on chosen parameters, providing insights into the most
  suitable versions.

- **Speckle Parts Panel**: Lists individual model components, including part counts per group. It
  offers detailed information for each component, such as cost, material, and lifecycle data, giving
  users a comprehensive overview of the model's structure.

## Main Systems

### Rhino Compute

This service provides a cloud-based, `stateless REST API` for performing geometry calculations on
various objects like points, curves, surfaces, meshes, and solids. It offers extensive access to
over 2400 RhinoCommon API calls, including unique functions like closest point and intersection
calculations. The solution supports integration with Rhino/Grasshopper plugins and allows
serialization of operations through `Grasshopper or Python scripts`. Additionally, client libraries
are available for use in standalone applications built in C# (.NET), Python, and
JavaScript.

The script hosted in
the [compute.rhino3d.appserver](https://github.com/mcneel/compute.rhino3d.appserver) repository has
unique input and output
characteristics. Both use
Speckle components to read and send working versions. The key components are:

- Read Component: Retrieves geometry from the Speckle server.
- Manufacturer Geometrical Logic: Generates geometry based on manufacturer constraints.
- Send Component: Sends geometry to the Speckle server.
- Visualize Component: Displays geometry in the appserver.

![Dolcker Constructive System](src/static/assets/viewport2.png)
*Figure 2: Visualization of the Dolcker Constructive System in the application (view from the
wall to the outside -insulation, angular, t vertical profile, dolcker horizontal profile, panel-).*


<img src="src/static/assets/gh_def2.png" alt="Grasshopper Script" style="width: 100%;">

*Figure 3: Grashopper Script used inside the Appserver repository (profile definition, input
surface, tridimensional constructive system).*

### Speckle Systems

[Speckle](https://speckle.systems/) provides a `version control system` for all baked geometry and
is useful for managing
geometry, associated data and
their
variations. The Speckle iframe is used to display geometry and its variations in the web
application.

Speckle plays a crucial role in the project by managing client input geometry, building the
infrastructure to store its data along with associated metadata, and providing an intuitive way to
interact within its python integration. Additionally, Speckle facilitates storing the
output geometry and metadata from the Rhino Compute service, allowing this updated information to be
returned to the **original tool where the client is working**.

- **Geometry**: Created by Grasshopper and Rhino Compute.
- **System Parts**: Components associated with the geometry.
- **Part Data**: Data linked with each system part.
- **Metadata**: Additional data about geometry.

Further Steps:

- Resolve the Speckle read component failure in Grasshopper.
- [Deploy the Speckle Server](https://speckle.guide/dev/server-manual-setup.html)

```mermaid
graph LR
    CLIENT_INPUT_GEOMETRY -->|processed by| RHINO_COMPUTE
    CLIENT_INPUT_GEOMETRY -->|stores| SPECKLE
    RHINO_COMPUTE -->|creates| TRANSFORMED_SURFACE
    TRANSFORMED_SURFACE -->|stores| SPECKLE
    SYSTEM_PARTS -->|associates| SPECKLE
    PART_DATA -->|associates| SPECKLE
```

*Diagram 2: Specific interaction login within Speckle service.*

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

The input data is a surface that represents the facade of a building. The output data is a 3D
model of the facade with the Dolcker & Clip system applied. The **Rhino/Grasshopper connectors** by
Speckle are used to read and send the geometry data to
the [Speckle server](https://app.speckle.systems/projects/013613abb4/models/8d916b252e).

![Compute Version Control](src/static/assets/readme.png)
*Figure 4: Input model from Grasshopper into the Speckle Server using the connectors.*

### Relational Database

This project uses `PostgreSQL` as the primary database systems to reflect the business logic
of the project. It stores and
manages
construction related data, users and interactions.

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

```mermaid
erDiagram

%% Users and Projects
    users ||--o{ projects: "owns"
    users ||--o{ parameter_configurations: "creates"
    users ||--o{ user_interactions: "performs"
    projects ||--o{ parameter_configurations: "has"
    projects ||--o{ speckle_projects: "linked to"
    projects ||--o{ user_interactions: "involves"
%% Parameter Configurations and Products
    parameter_configurations ||--o{ parameter_configuration_products: "includes"
    parameter_configuration_products }o--|| product_variants: "configures"
    product_variants }o--|| products: "variant of"
    parameter_configuration_products ||--o{ parameter_configuration_attributes: "has attributes"
    parameter_configuration_attributes }o--|| product_attributes: "configures"
%% Speckle Data
    speckle_projects ||--o{ speckle_branches: "contains"
    speckle_branches ||--o{ speckle_commits: "has"
%% Commits
    parameter_configurations ||--o{ commits: "generates"
    commits ||--|| speckle_commits: "links to"
%% Manufacturer Metadata
    manufacturers ||--o{ series: "offers"
    series ||--o{ products: "includes"
    series ||--o{ colors: "has"
    products ||--o{ product_variants: "has variants"
    products }o--|| series: "belongs to"
    product_variants }o--|| colors: "has color"
    product_variants }o--|| finishes: "has finish"
    product_variants }o--|| thicknesses: "has thickness"
    product_variants }o--|| applications: "has application"
    product_variants }o--|| systems: "has system"
    products ||--o{ product_attributes: "has"
    project_elements ||--|| products: "uses"
%% Entities
    users {
        int user_id PK
        varchar first_name
        varchar last_name
        varchar email
        date last_connection
        date created_at
        date updated_at
    }

    projects {
        int project_id PK
        int user_id FK
        varchar project_name
        text project_description
        date created_at
        date updated_at
    }

    parameter_configurations {
        int parameter_configuration_id PK
        int user_id FK
        int project_id FK
        date created_at
        date updated_at
    }

    parameter_configuration_products {
        int parameter_configuration_product_id PK
        int parameter_configuration_id FK
        int product_variant_id FK
    }

    parameter_configuration_attributes {
        int parameter_configuration_attribute_id PK
        int parameter_configuration_product_id FK
        int product_attribute_id FK
        varchar selected_value
    }

    product_attributes {
        int product_attribute_id PK
        int product_id FK
        varchar attribute_name
    }

    products {
        int product_id PK
        int manufacturer_id FK
        int series_id FK
        varchar product_name
        text product_description
    }

    product_variants {
        int product_variant_id PK
        int product_id FK
        int color_id FK
        int finish_id FK
        int thickness_id FK
        int application_id FK
        int system_id FK
    }

    series {
        int series_id PK
        int manufacturer_id FK
        varchar series_name
    }

    colors {
        int color_id PK
        int series_id FK
        varchar color_name
    }

    finishes {
        int finish_id PK
        varchar finish_name
    }

    thicknesses {
        int thickness_id PK
        varchar thickness_name
        decimal thickness_value
    }

    applications {
        int application_id PK
        varchar application_name
    }

    systems {
        int system_id PK
        varchar system_name
        text description
    }

    commits {
        int commit_id PK
        int parameter_configuration_id FK
        int speckle_commit_id FK
        varchar message
        date created_at
        date updated_at
    }

    user_interactions {
        int interaction_id PK
        int user_id FK
        int project_id FK
        int parameter_configuration_id FK
        date interaction_time
    }

    speckle_projects {
        int speckle_project_id PK
        int project_id FK
        varchar name
        date created_at
        date updated_at
    }

    speckle_branches {
        int speckle_branch_id PK
        int speckle_project_id FK
        varchar name
        text description
        date created_at
        date updated_at
    }

    speckle_commits {
        int speckle_commit_id PK
        int speckle_branch_id FK
        varchar message
        text data
        date created_at
        date updated_at
    }

    manufacturers {
        int manufacturer_id PK
        varchar name
        text description
    }

%% Connecting Products to Project Elements
    project_elements {
        int element_id PK
        int project_id FK
        int product_id FK
        int quantity
        varchar element_name
        text element_description
        date created_at
        date updated_at
    }
```

*Diagram 3: Proposed database structure for the project to enable faster and more scalable data
ingestion.*

In this diagram:

- **Users and Projects**:
    - `users` represents platform users, storing personal and account-related information.
    - `projects` represents user-created projects, including project details and descriptions.
    - `user_interactions` records interactions between users and platform elements, such as projects
      or parameter configurations.

- **Parameter Configurations and Products**:
    - `parameter_configurations` stores configurations of parameters for products within projects.
    - `parameter_configuration_products` links parameter configurations to specific product
      variants.
    - `parameter_configuration_attributes` represents selected attributes for a product in a
      configuration.
    - `products` represents the catalog of products offered by manufacturers.
    - `product_variants` represents different variants of a product, defined by attributes like
      color, finish, etc.
    - `product_attributes` defines specific attributes for products, such as features or
      specifications.

- **Product Metadata**:
    - `series` represents a grouping of products under a specific manufacturer series.
    - `colors`, `finishes`, `thicknesses`, `applications`, `systems` define different attributes,
      capturing variations offered by manufacturers.

- **Commits and Speckle Data**:
    - `commits` tracks changes made to parameter configurations, linking them to Speckle commits.
    - `speckle_models` links internal projects to their representation in Speckle, containing
      metadata.
    - `speckle_commits` represents commits within a Speckle branch, tracking changes in data.

- **Manufacturers and Elements**:
    - `manufacturers` represents companies offering products within the platform.
    - `project_elements` links specific elements of a project to products used, including quantities
      and details.

> [!NOTE]
> The database structure is currently in development and will be updated in future iterations.
> The current local database is run locally in a SQLite3 file with only one table containing the
> parameters iterations and the commit message.

## Conclusion

`Compute Version Control` is a **work in progress** that offers a powerful solution for managing and
validating
design
proposals,
enhancing the efficiency and accuracy of the design process. By leveraging the combined capabilities
of Rhino Compute, Speckle, and PostgreSQL, the system provides a **comprehensive approach to version
control and systems data on testing iteration** project designs. The main focus areas for the near
future are:

- **Ease of Use**: Improve the user interface for a more intuitive and user-friendly experience.
  Users can simply select the manufacturer and system they wish to test, run the computation, and
  load the results into their preferred tool.
- **Business Intelligence**: Create advanced analytics and reporting features to provide
  manufacturers with valuable insights.
