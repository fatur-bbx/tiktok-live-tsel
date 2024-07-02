import json
import os
import subprocess
import signal
import asyncio
import threading
import sys
from datetime import datetime
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent

# Ensure the data directory exists
os.makedirs('./result/chat', exist_ok=True)

# Function to create a client for a specific username
def create_client(username):
    client = TikTokLiveClient(unique_id=username)

    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{current_time}_{username.replace('@', '')}.json"
    file_path = os.path.join('./result/chat', filename)

    # Initialize the JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump([], f)

    @client.on(ConnectEvent)
    async def on_connect(event: ConnectEvent):
        print(f"Connected to @{event.unique_id} (Room ID: {client.room_id})")
        if client.is_live:
            command = f"python ./main.py -ffmpeg -room_id {client.room_id} -output ./result/video/media/"
            proc = subprocess.Popen(command, shell=True)
            client.subprocesses.append(proc)

    @client.on(CommentEvent)
    async def on_comment(event: CommentEvent):
        comment_data = {
            "username": event.user.nickname,
            "comment": event.comment
        }
        with open(file_path, 'r+', encoding='utf-8') as f:
            file_data = json.load(f)
            file_data.append(comment_data)
            f.seek(0)
            json.dump(file_data, f, ensure_ascii=False, indent=4)

    return client

client1 = create_client("@natashaskincare.id")
client2 = create_client("@erigo.store")
client3 = create_client("@kleaner.indonesia")

# Store subprocesses for each client
client1.subprocesses = []
client2.subprocesses = []
client3.subprocesses = []

def signal_handler(sig, frame):
    print("CTRL + C detected. Stopping all subprocesses...")
    for client in [client1, client2, client3]:
        for proc in client.subprocesses:
            proc.send_signal(signal.SIGINT)
    loop.call_soon_threadsafe(loop.stop)
    print("Program stopped.")

async def cekLive(client):
    return await client.is_live()

def start_clients():
    global loop  # Gunakan loop sebagai variabel global di sini
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if cekLive(client1):
        loop.create_task(client1.start())
    if cekLive(client2):
        loop.create_task(client2.start())
    if cekLive(client3):
        loop.create_task(client3.start())
    loop.run_forever()

if __name__ == '__main__':
    try:
        start_clients()
    except KeyboardInterrupt:
        signal.signal(signal.SIGINT, signal_handler)
    