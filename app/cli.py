import argparse
from .config import Config


def cli_runner(config: Config):
    parser = argparse.ArgumentParser(description="PhoneWave CLI")
    parser.add_argument("-e", "--env", nargs="+", help="Environment variables to set")

    args = parser.parse_args()
    env_variables = args.env

    for env_variable in env_variables:
        key, value = env_variable.split("=")
        variables = {key: value}

        config.overwrite(**variables)
