# FastAPI and Databricks Lakehouse CRUD Example

A FastAPI example using a Databricks backend. The goal is to demonstrate that FastAPI can be connected with the Databricks Lakehouse architecture and perform CRUD activities.

## Setup

This example uses Poetry. Install [Poetry](https://python-poetry.org/) and run `poetry install` to install the dependenices.

### Prerequisites

1. Have access to a Databricks Workspace
2. An existing cluster or SQL warehouse
3. Can create a Databricks PAT token

### Configuration

Follow the [Databricks Guide](https://docs.databricks.com/dev-tools/python-sql-connector.html#get-started) to collect the below cluster details:
- **Server Hostname**
- **HTTP Path**
- **PAT Token**

Add those values into a `.env` file similar to the one provided in `.env.example`

(Optional) Make sure the cluster you are targeting is already on. If the cluster is off, the first response will take additional time waiting for the cluster to come online.

### Create Fake User Data

Import the `.dbc` file under '/data/create_faker_data.dbc' into your Databricks workspace and run the notebook. This will create a Delta table for `users` under the a dataabase `fastapi`.

## Run FastAPI

In the parent folder of this repo run the below command to start the FastAPI server.

`uvicorn app.main:app --reload`

And you're all set! You now have a FastAPI running on a Lakehouse

## Acknowledgements

This example depends [sqlalchemy-databricks](https://github.com/crflynn/sqlalchemy-databricks) created by [crflynn](https://github.com/crflynn).

It is a thin wrapper for the [databricks-sql-connector](https://docs.databricks.com/dev-tools/python-sql-connector.html) and the [PyHive SQLAlchemy](https://github.com/dropbox/PyHive#sqlalchemy) libraries