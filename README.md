# Welcome to Hedge

## Local Environment Setup

Create a virtual environment and activate it in the shell

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install the necessary requirements from requirements.txt

```shell
pip3 install -r requirements.txt
```

Create the log folder. Locally, logs will be written to `logs/python.log`

```shell
mkdir logs
```

Create a _.env_ file in the project root directory and add the following keys (the API keys are listed on the Sharp
Sports account settings page).

```
SHARPSPORTS_PUBLIC_API_KEY=
SHARPSPORTS_PRIVATE_API_KEY=
MONGO_CLUSTER=HedgeCluster
MONGO_DB=hedge_test
MONGO_USER=hedge-nico
MONGO_PASSWORD=hedge2024
MONGO_API_KEY=<mongo_api_key>
GOOGLE_DRIVE_DATA_FOLDER_ID=<google_drive_folder_id>
```

### Debugging
If you get a `ModuleNotFound` error when running the scripts above you may need to add the project root to your 
python path. Run `export PYTHONPATH="PROJECT_ROOT:$PTYHONPATH"` and replace `PROJECT_ROOT` with the correct path 
to the hedge project root.


## Testing

We use pytest for unit testing and unittest patch for mocking values. To run all tests use the following commands from
the project root

```shell
pytest tests
```
