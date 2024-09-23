import hashlib
import json

USERS_FILE = 'users.json'
users = {}

def load_users_from_file():
    global users
    try:
        with open(USERS_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                users = json.loads(content)
    except FileNotFoundError:
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
        users = {}

def save_users_to_file():
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f)
    except Exception as e:
        print(f"Error saving users: {e}")

def register_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users:
        print(f"Username {username} is already taken.")
    else:
        users[username] = hashed_password
        save_users_to_file()

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users:
        if users[username] == hashed_password:
            return True
    return False
