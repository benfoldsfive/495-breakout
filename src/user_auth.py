"""
User Authentication Logic
--------------
Handles the methods and systems for user authentication, including the
JSON users file.
"""

import hashlib
import json

USERS_FILE = 'users.json'
users = {}

def load_users_from_file():
    """
    Loads user data from a JSON file into the global 'users' dictionary.

    If the file doesn't exist or is empty, it initializes an empty users file.

    This function is intended to be called when the program starts to retrieve
    any previously saved user data (usernames, hashed passwords, and high scores).
    """
    global users
    try:
        with open(USERS_FILE, 'r') as f:
            content = f.read().strip()
            if content:
                users = json.loads(content) # Load user data if content exists
    except FileNotFoundError:
        # If the file is not found, create a new one and initialize an empty dictionary
        with open(USERS_FILE, 'w') as f:
            json.dump({}, f)
        users = {}

def save_users_to_file():
    """
    Saves the current user data (usernames, hashed passwords, and high scores)
    to the JSON file defined by USERS_FILE.

    This function is called after updating or registering users to persist
    the changes on disk.
    """
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f) # Write user data to file
    except Exception as e:
        print(f"Error saving users: {e}") # Handle any file writing errors

def register_user(username, password):
    """
    Registers a new user by adding their username and hashed password to the 'users' dictionary.

    Arguments:
            - username: The username to register.
            - password: The plain-text password to be hashed and stored.

    This function checks if the username is already taken. If not, it hashes
    the password and saves the new user with a default high score of 0.
    Calls save_users_to_file() to persist the data.

    Prints messages for registration success or if the username is already taken.
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest() # Hash the password using SHA-256

    if username in users:
        print(f"Username {username} is already taken.")
    else:
        users[username] = {
            "password": hashed_password,
            "high_score": 0  # Initialize high score to 0 when registering
        }
        print(f"User {username} registered!")
        save_users_to_file() # Save new user data to the file

def login_user(username, password):
    """
    Verifies user login by checking the provided password against the stored hashed password.

    Arguments:
        - username: The username attempting to log in.
        - password: The plain-text password to verify.

    Returns:
        - bool: True if login is successful, False otherwise.

    The password is hashed and compared to the stored hash. If the user exists
    and the passwords match, login is successful.
    """
    hashed_password = hashlib.sha256(password.encode()).hexdigest() # Hash the entered password
    if username in users:
        if users[username]["password"] == hashed_password: # Check if hashed passwords match
            return True
    return False

def update_high_score(username, score):
    """
    Updates a user's high score if the new score is higher than the current high score.

    Arguments:
        - username: The username whose score is being updated.
        - score: The new score to compare against the user's current high score.

    This function checks if the user exists and updates their high score only
    if the new score is greater than the previously stored high score.
    Calls save_users_to_file() to persist the update.
    """
    if username in users:
        if score > users[username]["high_score"]:
            users[username]["high_score"] = score  # Update high score if new score is higher
            save_users_to_file()  # Save the updated high score
            print(f"High score updated for {username}!")
    else:
        print(f"User {username} not found.")

def get_high_score(username):
    """
    Retrieves the high score for a given username.

    Arguments:
        - username: The username whose high score is being requested.

    Returns:
        - int or None: The high score for the user, or None if the user doesn't exist.

    This function checks if the user exists and returns their stored high score.
    If the user is not found, it prints a message and returns None.
    """
    if username in users:
        return users[username]["high_score"] # Return the user's high score
    else:
        print(f"User {username} not found.")
        return None
