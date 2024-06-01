import discord
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import re
import os
import json
from dotenv import load_dotenv
import threading

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Load server details from JSON file
with open('servers.json', 'r') as f:
    servers = json.load(f)

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

THUMBNAIL_URL = 'https://media.discordapp.net/attachments/932110907729920080/1245453724088795146/unnamed.png?ex=6658ceab&is=66577d2b&hm=b7428e76fc490179f054b831f6b0c36e41af4ab7b0e1d868f7584cdb3d080880&=&format=webp&quality=lossless&width=400&height=400'

class LogHandler(FileSystemEventHandler):
    def __init__(self, server_name, channel_id, loop):
        self.server_name = server_name
        self.channel_id = channel_id
        self.loop = loop
        self.positions = {}

    def set_initial_position(self, path):
        self.positions[path] = os.path.getsize(path)

    def process(self, event):
        if event.event_type == 'modified':
            with open(event.src_path, 'r') as file:
                # Move to the position we left off at, or the start if not known
                file.seek(self.positions.get(event.src_path, 0))
                lines = file.readlines()
                self.positions[event.src_path] = file.tell()  # Update the position

                for line in lines:
                    if 'LogTemp: Rcon:' in line:
                        timestamp = re.search(r'\[(.*?)\]', line).group(1)
                        rcon_command = line.split('LogTemp: Rcon: ')[1].strip()

                        # Ignore InspectPlayer, ServerInfo, and RefreshList commands
                        if 'InspectPlayer' in rcon_command or 'ServerInfo' in rcon_command or 'RefreshList' in rcon_command:
                            continue

                        asyncio.run_coroutine_threadsafe(self.send_message(timestamp, rcon_command), self.loop)

    async def send_message(self, timestamp, rcon_command):
        channel = client.get_channel(self.channel_id)
        if channel:
            embed = discord.Embed(title="Rcon Command Detected", color=0xff0000)
            embed.set_thumbnail(url=THUMBNAIL_URL)
            embed.add_field(name="Server", value=self.server_name, inline=False)
            embed.add_field(name="Timestamp", value=timestamp, inline=False)
            embed.add_field(name="Command", value=rcon_command, inline=False)
            await channel.send(embed=embed)

    def on_modified(self, event):
        self.process(event)

async def start_bot():
    await client.start(TOKEN)

def start_observer(loop):
    observer = Observer()
    handlers = []

    for server_name, server_info in servers.items():
        event_handler = LogHandler(server_name, server_info['channel_id'], loop)
        event_handler.set_initial_position(server_info['path'])
        handlers.append(event_handler)
        observer.schedule(event_handler, path=os.path.dirname(server_info['path']), recursive=False)

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    observer_thread = threading.Thread(target=start_observer, args=(loop,))
    observer_thread.start()

    loop.run_until_complete(start_bot())
