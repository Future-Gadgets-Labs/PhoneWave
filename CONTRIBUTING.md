# Contributing Rules

- Ensure all **Python** features used in this project works in Python 3.10 and above.

- Tell us what you are planning before you start.

- Each new peice of code you add should be:
    - documented, at least self explanatory.
    - and tests should be added, and must pass.


> this ensure that we don't break each other's code ...

- Be nice, not everyone is a python expert with 800 years of experience, suggestions are welcomed.

- We configured this project with a particular workflow, this ensure the quality of the code. 
> We kindly ask you to follow this workflow.


# Getting Started

This guide assumes you are already familair with Discord's bot API and already have a bot account
and already have some experience working with python.

Requirements:
- Python 3.10+
- git
- pip or pipenv

## Project setup 

1. create a `.env` file in the root of the project, take a look on the example file [here](./.env.example)

Using pipenv ( recommended ):
```bash
pipenv install
--> pipenv will do all the magic
```

Using pip:
```bash
--> for "windows" users
> python -m venv .venv
> ./.venv/scripts/activate
> pip install -r requirements.txt

--> for "linux" users
> python3 -m venv .venv
> source ./.venv/bin/activate
> pip install -r requirements.txt
```

### Running the bot

**Pipenv**
```bash
pipenv run bot
```

**Pip**
```bash
--> for "windows" users
> python ./main.py

--> for "linux" users
> python3 ./main.py
```

Then you shoud see something like this
```
2069-04-05 09:55:55 | info     | Starting up...
2069-04-05 09:55:55 | info     | Loaded 8 extentions
2069-04-05 09:55:55 | info     | Logged in as [BotUsername #1234]
```
