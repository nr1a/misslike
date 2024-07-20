import threading
import requests
import random
import string
import os
import signal
import time
from api import api, create, follow
from dotenv import load_dotenv

load_dotenv()

# Configuration
NUM_THREADS = 5
INSTANCE = os.getenv("instance")
MASTER_TOKEN = os.getenv("master_token")
USER_ID = os.getenv("userId")
CREATE_URL = INSTANCE + api.create
FOLLOW_URL = INSTANCE + api.follow
follower_count = 0
TOKENS_FILE = "tokens.txt"
threads = []
stop_threads = False


def generate_random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def create_account():
    username = generate_random_string()
    password = generate_random_string()
    create_data = create(username, password, MASTER_TOKEN).get_data()
    response = requests.post(CREATE_URL, json=create_data)
    response.raise_for_status()
    return response.json()["token"]


def follow_user(token):
    follow_data = follow(USER_ID, token).get_data()
    response = requests.post(FOLLOW_URL, json=follow_data)
    response.raise_for_status()


def save_token(token):
    with open(TOKENS_FILE, "a") as f:
        f.write(token + "\n")


def run_spam_follow():
    global follower_count
    while not stop_threads:
        try:
            print("Creating account...")
            token = create_account()

            print("Following...")
            follow_user(token)

            save_token(token)

            follower_count += 1
            print(f"Follower count: {follower_count}")

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            break


def signal_handler(sig, frame):
    global stop_threads
    print("Stopping threads...")
    stop_threads = True
    for t in threads:
        t.join()
    print("All threads stopped. Exiting...")
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


for _ in range(NUM_THREADS):
    t = threading.Thread(target=run_spam_follow)
    t.start()
    threads.append(t)

while not stop_threads:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)
