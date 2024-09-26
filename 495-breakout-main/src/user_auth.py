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
        users[username] = {
            "password": hashed_password,
            "high_score": 0  # Initialize high score to 0 when registering
        }
        save_users_to_file()

def login_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if username in users:
        if users[username]["password"] == hashed_password:
            return True
    return False

def update_high_score(username, score):
    if username in users:
        if score > users[username]["high_score"]:
            users[username]["high_score"] = score  # Update high score if new score is higher
            save_users_to_file()
            print(f"High score updated for {username}!")
    else:
        print(f"User {username} not found.")

def get_high_score(username):
    if username in users:
        return users[username]["high_score"]
    else:
        print(f"User {username} not found.")
        return None
