# Multi Stage build ftw
FROM python:3-slim-bullseye as deps
WORKDIR /home/phonewave

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM python:3-slim-bullseye
COPY --from=deps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /home/phonewave

COPY . .

CMD ["python", "main.py"]