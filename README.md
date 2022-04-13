# PhoneWave

PhoneWave is a Discord bot written in Python that tears through the fabric of time and space to deliver all the Discord needs a mad scientist might have. You can find us in our [Laboratory](https://discord.gg/nAqaXhpafP).

## For Developers


### Base setup

1. Create a ".env" and override any required variables appropriately (like `BOT_TOKEN`).

### Running with Docker

1. Install Docker - https://docker.com/get-started/****
2. Run `docker-compose up -d` on the project root directory (where the `docker-compose.yml` file is present). This will start the bot and mongo services in the background.
3. Run `docker-compose logs -f bot` if you wish to see the bot logs.

Building an image locally:
1. Create the Docker image with `docker-compose build`. This creates an image named "phonewave:latest" 
2. Tag the image with your DockerHub username: `docker image tag phonewave:latest your-username/phonewave:latest`
3. Push image to DockerHub: `docker push your-username/phonewave:latest`

### Running locally

1. Install Python 3.9+ - https://python.org/downloads/
2. Create a virtual environment with `python -m venv .venv` and activate it with `source .venv/bin/activate` (Linux) or `.venv\Scripts\activate.bat` (Windows)
3. Install dependencies with `pip install -r requirements.txt`
4. Start bot with `python main.py`

## Ways to help

- **Improve Documentation:** Adding missing information, fixing typos, etc.
- **Feedback:** Report bugs, request features, etc.
- **Contribute:** Propose new features, or find an existing one. 

### Contributing Workflow

- Tell us what you are planning before you start.
- Fork the repository
- Make changes to the code
- Run all the test, check that all of them passed.
- Make a pull request 
- Your PR is Merged, you are now a supahacka.
