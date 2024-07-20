import requests
import time
import os
import signal
from api import api, reactions
from dotenv import load_dotenv

load_dotenv()

instance = os.getenv("instance")
noteId = os.getenv("noteId")
reaction = "❤️"
url = instance + api.reactions
tokens_file = "tokens.txt"
stop_process = False


def signal_handler(sig, frame):
    global stop_process
    print("Stopping process...")
    stop_process = True


signal.signal(signal.SIGINT, signal_handler)


with open(tokens_file, "r") as f:
    tokens = f.read().splitlines()


start_time = time.time()


for token in tokens:
    if stop_process:
        break
    try:

        data = reactions(noteId, reaction, token).get_data()

        response = requests.post(url, json=data)

        end_time = time.time()

        execution_time = end_time - start_time

        print(response)

        if response.status_code not in [204, 400]:
            print(f"Unexpected status code: {response.status_code}")
            break

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        break

print(f"Execution time: {execution_time} seconds")
