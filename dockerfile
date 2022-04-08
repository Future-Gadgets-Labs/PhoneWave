# Multi Stage build ftw
FROM python:3-slim-bullseye as deps
WORKDIR /home/phonewave

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

FROM python:3-slim-bullseye
COPY --from=deps /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /home/phonewave

# Copy app code
COPY . .

# Start bot
CMD ["python3", "main.py"]