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

Create the output folders. These are required for exporting bet data and stats. If they do not exist, the scripts will
fail!

```shell
mkdir out
mkdir out/betslips_raw
mkdir out/betslips_formatted
mkdir out/stats
```

Create a _.env_ file in the project root directory and add the following keys (the API keys are listed on the Sharp
Sports account settings page).

```
SHARPSPORTS_PUBLIC_API_KEY=
SHARPSPORTS_PRIVATE_API_KEY=
FANDUEL_NY_ID=BRGN_ab5628fa79344c39bce8fec0f17fbdcc
DRAFTKINGS_NY_ID=BRGN_b28ee954c84f4668bd4b7763beb90a97
UNDERDOG_NY_ID=BRGN_1f575e712ade47dfb4891e2959c60250
```

## Running the Scripts

There are three total Python scripts

### _get_custom_url.py_

Creates a custom url to link a sportsbook account for a given user and sportsbook. To get usage
run `python3 betsync/get_custom_url.py help`.

### _fetch_betslips.py_

Fetches betslips (all time) from the Sharp Sports API for a given user. To get usage
run `python3 betsync/fetch_betslips.py help`.

### _calculate_stats.py_

Calculates ROI and Average Unit for a given user, grouped by Bet Type, for all time bets. To get usage
run `python3 hedge/calculate_stats.py help`.

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
