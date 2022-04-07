# Multi Stage build ftw
FROM python:3.9.9-slim-buster as deps

WORKDIR /PhoneWave

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM python:3.9.9-slim-buster
COPY --from=deps /opt/venv /opt/venv
ENV PATH="opt/venv/bin:$PATH"

WORKDIR /PhoneWave

# Should only copy what we need ( would be a security flaw to copy everything )
COPY ./app ./main.py ./.env ./.env.development ./

CMD ["main.py"]