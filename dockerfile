FROM python:3-slim-buster

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy app code
COPY . .

# Start bot
CMD ["python3", "main.py"]