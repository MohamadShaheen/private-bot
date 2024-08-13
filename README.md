# Introduction

This is a telegram-bot that represents a game about many topics. The project heavily relies on external APIs and request-response module.

# Instructions

- In order to fetch the [BOT_TOKEN](#installation) environment variable refer to [fetch bot token](https://core.telegram.org/bots/features#botfather).

# Features

- Get random question.
- Get questions by filter.
- Get all categories.

# Technologies Used

- python-telegram-bot
- requests
- MongoDB

# Requirements

- Python 3.8+

# Installation

1. **Clone the repository:**
   ```shell
    git clone https://github.com/MohamadShaheen/private-bot.git
    cd private-bot
    ```
   
2. **Setup the virtual environment:**
   ```shell
   python -m venv venv
   venv/Scripts/activate # On Mac/Linux `source venv/bin/activate`
    ```
   
3. **Install dependencies:**
    ```shell
    pip install -r requirements.txt
    ```
   
4. **Set up environment variables:** Create a `.env` file in the project root directory and add the following environment variables:
    ```shell
    BOT_TOKEN=<your-bot-token>
    SERVER_URL=<your-server-url-for-requests> # For example: `http://localhost:8000`
    ```
   
# Project Logs

Make sure to create a directory named `logs` in the project root directory:
   ```shell
   mkdir "logs"
   ```

# Running the Bot

   ```shell
   python bot.py
   ```

