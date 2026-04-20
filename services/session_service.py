import json
import os

SESSION_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "session.json")


def save_session(username):
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)


def load_session():
    if not os.path.exists(SESSION_FILE):
        return None

    with open(SESSION_FILE, "r") as f:
        data = json.load(f)
        return data.get("username")


def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)