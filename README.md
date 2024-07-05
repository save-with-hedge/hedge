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

## Testing
We use pytest for unit testing and unittest patch for mocking values. To run tests use the following commands from 
the project root
```shell
pytest tests # for running all tests
```
