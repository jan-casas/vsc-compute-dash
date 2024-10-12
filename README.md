# Unlocking Business Intelligence for AEC Manufacturers with Compute Version Control

**Compute Version Control (VSC)** is an innovative tool that enhances flexibility in the
Architecture, Engineering, and Construction (AEC) sector. It allows architects and designers to
quickly test parametric manufacturer solutions directly within their preferred tools. By integrating
manufacturer-provided constraints, VSC validates design proposals and delivers essential information
on cost, material specifications, geometrical constraints, and lifecycle data. This enables informed
decision-making and ensures compliance with industry standards.

VSC also provides manufacturers with valuable business intelligence by offering insights into how
their products are used and understanding customer needs. The system leverages Rhino Compute for
geometry generation, Speckle for version control and data management, and a relational database for
associating geometry with lifecycle data. This integrated approach streamlines workflows, enhances
efficiency, and contributes to more sustainable and cost-effective construction solutions in the AEC
industry.

https://github.com/user-attachments/assets/80194026-07dd-47c5-b0f2-0c975b7fa086

*Figure 1: Landing page of the Webapp. You can see the Compute and Speckle window and the params
to interact with.*

### Table of Contents

- [Overview](#overview): Summary of the project, including the problem it addresses, key features,
  and the proposed software architecture.
    - [Problem Statement](#problem-statement): Challenges in the AEC industry and the need for
      better design validation and collaboration.
    - [Business Intelligence](#business-intelligence): Benefits of the solution, such as improved
      decision-making and data-driven insights.
    - [Software Architecture](#software-architecture): Proposed architecture using Rhino Compute,
      Speckle, and a relational database.
- [Project Structure](#project-structure): Overview of the project’s main components and input data.
    - [Input Data](#input-data): Description of input data, specifically a building facade surface.
    - [User Interface](#user-interface): Overview of the user interface, including the landing page
      and side panels.
- [Core Systems](#core-systems): Explanation of the key systems used in the project.
    - [Rhino Compute](#rhino-compute): Role of Rhino Compute in generating geometry data based on
      manufacturer constraints.
    - [Speckle](#speckle): How Speckle handles geometry, variations, and version control.
    - [Relational Database](#relational-database): Role of the database in storing geometry data,
      parameters, and system data.
- [Conclusion](#conclusion): Recap of key features and next steps for project development.
    - [Next Steps](#next-steps): Future development focus on usability, business intelligence,
      deployment, performance, and scalability.

## Overview

### Problem Statement

The Architecture, Engineering, and Construction (AEC) industry faces challenges in efficiently
testing and validating design proposals. Architects and designers often struggle to integrate
standard manufacturer constraints into their designs, leading to inefficiencies and inaccuracies.

- **Enhanced Design Validation**: Validate design proposals by integrating manufacturer constraints
  and generating geometry data.
- **Improved Collaboration**: Facilitate collaboration between architects and manufacturers by
  providing a platform for testing and validating design proposals.
- **Cost-Efficient Solutions**: Enable architects to test parametric solutions and select materials
  based on cost and lifecycle data.

### Business Intelligence

This method allows manufacturers to gain valuable insights into how their products are used and how
they can improve their offerings. By analyzing data on material specifications, geometrical
constraints, and lifecycle data, manufacturers can make informed decisions and enhance their product
offerings.

- **Enhanced Decision-Making**: Access to detailed material lifecycle data allows for better
  material selection and project planning.
- **Improved Compliance**: Ensures designs meet manufacturer constraints and industry regulations.
- **Data-Driven Insights**: Robust data management enables valuable insights from project
  interactions.
- **Streamlined Workflow**: Automates design validation and management, reducing manual effort.
- **Scalability**: Modular architecture easily scales with growing business needs.

```mermaid
graph LR
    A[Challenges in AEC Industry]
%% Core Clusters
    A -->|Needs| B[Design Validation & Collaboration]
    A -->|Requires| C[Cost-Efficiency]
    B -->|Integrates| D[Manufacturer Constraints]
    B -->|Facilitates| E[Collaboration between Architects and Manufacturers]
    C -->|Optimizes| F[Material Selection & Lifecycle Costs]
%% Business Intelligence Cluster
    D -->|Feeds| G[Business Intelligence]
    E -->|Produces| G
    F -->|Generates| G
%% Business Intelligence Benefits
    G -->|Enables| H[Better Decision-Making]
    G -->|Ensures| I[Compliance]
    G -->|Automates| J[Workflows]
    G -->|Scales| K[Solution Growth]


```

*Diagram 1: Conceptual diagram about the challenges and opportunities for manufacturers in the
AEC industry.*

### Software Architecture

The proposed architecture leverages Rhino Compute for geometry generation, Speckle for version
control and data management, and a relational database for associating geometry with lifecycle data.
The application comprises three main components:

- **Rhino Compute**: Generates constructive solutions by handling predefined manufactured systems.
- **Speckle**: Acts as a data repository for storing geometry, managing IDs, variations, and
  providing filtering tools.
- **Relational Database**: Associates geometry IDs with lifecycle data for efficient tracking and
  retrieval.

This robust solution enhances accuracy and efficiency in managing and validating design proposals by
leveraging manufacturer-provided constraints.

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

### Scope of the Project

The project aims to develop a **minimum viable product** (MVP) to test the interaction and the link
with the Business Intelligence (BI) of the manufacturers. Only the Dolcker & Clip system by
Dolcker is used and the project is only tested on a local machine and is not yet deployed to a
Windows Virtual Machine (Speckle Server, Rhino Compute).

This repository only develops the web application and the interaction with the Compute App Server
and the Speckle server.
For further information about the Compute App Server and Speckle, please refer to the
[Compute App Server repository]() and the [Speckle Systems repository]().

## Project Structure

The project needs **three running technologies in paralle**l: one for the Node.js project
(Appserver),
Rhino Compute and the Python project web application.
There is needed a tool to generate the geometry and the logic of the building (in this
case Grasshopper).
In this repository only the python web application is showcase.

- **Grasshopper Project**: The main tool for creating the geometry and the logic of the building.
- **Rhino Compute Project**: The server that generates the geometry data based on the manufacturer
  constraints.
- **Node.js Project**: App server, responsible for managing the geometry data and the user
  interactions.
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

### Input Data

The input data for the project consists of a surface representing the facade of a building. This
is a black ceramic with vertical textures. I need to adapt the default Dolcker & Clip system to
mimic the facade's texture and color.

<p align="center">
  <img src="src/static/assets/facade2.png" alt="Seductive facade reference" width="49%"/>
  <img src="src/static/assets/facade-test.gif" alt="Model facade" width="49%"/>
</p>



*Figure 2: Reference image of the facade to be replicated in the Dolcker & Clip system and the
model image.*

### User Interface

The main focus of this repository is to provide a user-friendly interface for architects to
import their facade designs and test with the manufacturers' systems.
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

## Core Systems

### Rhino Compute

This service provides a cloud-based, `stateless REST API` for performing geometry calculations on
various objects like points, curves, surfaces, meshes, and solids. The solution supports integration
with Rhino/Grasshopper plugins and allows
serialization of operations through `Grasshopper or Python scripts`.

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

![Web Application](src/static/assets/readme.png)
*Figure 4: Webapp landing page. Compute section where you can config the params of the
grasshopper script and setup the branch and message to commit.*


> [!NOTE]
> **Parametric vs. Block**: Defining the geometrical logic of the systems allows not only the
> placement of identical blocks in different positions, but also the creation of an informed system
> based on input geometrical constraints.

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

- **Input Geometry**: Input geometry provided by the client through Speckle from any software,
  in this example the facade surface was created using Grasshopper.
- **Manufacture Constructive System**: Parametric constructive systems generated by Rhino
  Compute. Capable of handling different geometrical constraints.
- **Metadata**: Additional data about the manufacture system associated to the client geometry.

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

![Speckle Web](src/static/assets/speckle-capture2.png)
*Figure 4: Capture of the speckle webapp [model](https://app.speckle.systems/projects/74e8bc79d7)
. This is baked inside the clients repo in another branch, including systems metadata and data
tree information from the grasshopper script.*

![Web Application](src/static/assets/readme.png)
*Figure 6: Speckle Optimal Commit section. Used the metadata of the commit and compute an
aggregation of key values. This data is display in a parcoord graph to graphically filter your
optimal commit to later display it.*

![Web Application](src/static/assets/readme.png)
*Figure 7: Speckle Parts. This section is a repertoire of graphs that showcase the elements
present in the model an attributes.*

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

[//]: # (<details>)

[//]: # (<summary>WIP Database Proposal</summary>)

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

[//]: # (</details>)

> [!NOTE]
> The database structure is currently in development and will be updated in future iterations.
> The current local database is run locally in a SQLite3 file with only one table containing the
> parameters iterations and the commit message.

## Conclusion

`Compute Version Control` is a **work in progress** that offers a powerful solution for managing and
validating design proposals, enhancing the efficiency and accuracy of the design process. By
leveraging the combined capabilities of Rhino Compute, Speckle, and PostgreSQL, the system provides
a **comprehensive approach to version control and data management for iterative project designs**.
The main focus areas for the near future are:

### Next Steps

- **Ease of Use**: Enhance the user interface to create a more intuitive and user-friendly
  experience. Users will be able to select the manufacturer and system they wish to test, run
  computations, and effortlessly load the results into their preferred tools.
- **Business Intelligence**: Develop advanced analytics and reporting features to provide
  manufacturers with valuable insights.
- **Deployment**: Deploy the system to a production server to enable real-time testing and
  collaboration.
- **Performance**: Optimize the system for faster computation and data retrieval, ensuring a
  seamless user experience.
- **Scalability**: Improve the system's scalability to accommodate a growing user base and
  increasing data volumes.
