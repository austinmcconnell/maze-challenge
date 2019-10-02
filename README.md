# Maze Solver

This solution is written using Python 3.7

I've crafted my solution to include the following elements:

- Depencency & virtualenv management via [Pipenv](https://pipenv.kennethreitz.org/en/latest/)
- Type hints with [MyPy](https://mypy.readthedocs.io/en/latest/) checking
- Unit tests using [PyTest](https://docs.pytest.org/en/latest/)
- Testing "factories" using [Factory Boy](https://factoryboy.readthedocs.io/en/latest/)
- Standarized code conventions using the [Pre-commit](https://pre-commit.com/) framework
- Debug logging enabled via an environment variable


## Installation

If you don't already have pipenv, install it with the following command.

```shell script
pip install pipenv
```

Install app dependencies

```shell script
pipenv install --dev
```

## Run maze solver

Activate the virtualenv created by pipenv

```shell script
pipenv shell
```

Run the maze solver

```shell script
python -m app.solver "mazes.txt"
```

Incase you have trouble getting the code to run, I've also included the answers in `answers.txt`

## Development mode

### Debug logging

Debug logging statements are supported to aid development.

To see the debug messages, either add the env var inline

```shell script
LOG_LEVEL=DEBUG python -m app.solver "mazes.txt"
```

or create a .env file with the following contents

```ini
LOG_LEVEL=DEBUG
```
and source the .env file before running the main solver command

### Testing

Tests are written using PyTest. Run tests with the following command

```shell script
pytest tests
```

You should get output similar to the following.

```shell script
(maze-challenge) austinmcconnell on Austin_MBP in ~/projects/maze-challenge
$ pytest
============================================================================================ test session starts =============================================================================================
platform darwin -- Python 3.7.4, pytest-5.2.0, py-1.8.0, pluggy-0.13.0
rootdir: /Users/austinmcconnell/projects/maze-challenge
collected 7 items

tests/test_maze.py .......
```

### Pre-commit checks

I have added a set of pre-commit checks (.pre-commit-config.yaml) to ensure my code passes a series of common checks and linters

If you want to run the checks yourself, first install the pre-commit hooks

```shell script
pre-commit install
```

Now the hooks have been configured in your `.git/hooks` folder. These checks will automatically be run each time code is commited.

To manually run the checks, use

```shell script
pre-commit run --all-files
```

You will get output similar to the following

```shell script
(maze-challenge) austinmcconnell on Austin_MBP in ~/projects/maze-challenge
$ pre-commit run --all-files
pyenv-implicit: found multiple pre-commit in pyenv. Use version 3.7.0.
Check python ast.........................................................Passed
Check that executables have shebangs.................(no files to check)Skipped
Check for merge conflicts................................................Passed
Debug Statements (Python)................................................Passed
Fix double quoted strings................................................Passed
Fix End of Files.........................................................Passed
Trim Trailing Whitespace.................................................Passed
pylint...................................................................Passed
mypy.....................................................................Passed
Verifying PEP257 Compliance..............................................Passed
seed isort known_third_party.............................................Passed
isort....................................................................Passed

```
