# Builds a Docker image for our bot
# Based on https://sourcery.ai/blog/python-docker/

FROM python:3-slim-bullseye as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base as deps

# Install pipenv and compilation dependencies
RUN python3 -m pip install --upgrade pipenv
RUN apt-get update && apt-get install -y --no-install-recommends git gcc

# Install python dependencies in /.venv
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base as runtime

# Copy virtual env from python-deps stage
COPY --from=deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Create and switch to a new user
RUN useradd --create-home phonewave
WORKDIR /home/phonewave
USER phonewave

# Install application into container
COPY . .

ENTRYPOINT ["python"]
CMD ["main.py"]