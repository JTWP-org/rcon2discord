# Rcon2Discord Bot

This is a Discord bot that monitors log files for game servers, extracts RCON commands from the logs, and sends this information to specified Discord channels.

## Features

- Monitors log files for game servers.
- Extracts RCON commands from log entries.
- Sends RCON command information to Discord channels.

## Installation

### Prerequisites

- Python 3.10 or higher
- Discord bot token

### Step-by-Step Guide

1. **Clone the Repository**

    ```sh
    git clone https://github.com/JTWP-org/rcon2discord.git
    cd rcon2discord
    ```

2. **Create and Activate a Virtual Environment**

    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up Configuration Files**

    - Create a `.env` file with the following content:

      ```env
      DISCORD_BOT_TOKEN=your_discord_bot_token
      ```

    - Create a `servers.json` file to specify the server details:

      ```json
      {
          "Pavlov Server 1": {
              "path": "/path/to/your/log/file1.log",
              "channel_id": "your_discord_channel_id_1"
          },
          "Pavlov Server 2": {
              "path": "/path/to/your/log/file2.log",
              "channel_id": "your_discord_channel_id_2"
          }
      }
      ```

5. **Run the Bot**

    ```sh
    python bot.py
    ```

## Configuration

### .env File

The `.env` file should contain your Discord bot token:

```env
DISCORD_BOT_TOKEN=your_discord_bot_token
