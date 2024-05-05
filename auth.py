import bcrypt
import pyotp
import qrcode
import getpass
import os
import uuid

# File to store users, hashed passwords, and TOTP secrets
PASSWORD_FILE = "passwords.txt"

def load_users():
    """
    Load the user data from the password file. 
    Each line in the file should be in the format: id:username:hashed_password:totp_secret
    Returns:
        dict: A dictionary where the key is the username and the value is another 
              dictionary containing 'id', 'hashed' (hashed password), and 'secret' (TOTP secret).
    """
    users = {}
    try:
        with open(PASSWORD_FILE, "r") as file:
            for line in file:
                user_id, username, hashed, secret = line.strip().split(":")
                users[username] = {'id': user_id, 'hashed': hashed.encode('utf-8'), 'secret': secret}
    except FileNotFoundError:
        pass
    return users

def save_user(username, hashed, secret, user_id):
    """
    Save a new user to the password file and create a user-specific file.
    
    Args:
        username (str): The username of the new user.
        hashed (bytes): The hashed password.
        secret (str): The TOTP secret.
        user_id (str): The ID of the user.
    """
    with open(PASSWORD_FILE, "a") as file:
        file.write(f"{user_id}:{username}:{hashed.decode('utf-8')}:{secret}\n")

    # Save user data in a separate file
    user_file = f"{username}_data.txt"
    with open(user_file, "w") as file:
        file.write(f"ID: {user_id}\n")
        file.write(f"Username: {username}\n")
        file.write(f"Secret: {secret}\n")

def generate_totp_secret():
    """
    Generate a new TOTP secret.
    
    Returns:
        str: A randomly generated TOTP secret.
    """
    return pyotp.random_base32()

def generate_qr_code(username, secret):
    """
    Generate and display a QR code for a TOTP secret.
    
    Args:
        username (str): The username of the new user.
        secret (str): The TOTP secret.
    """
    uri = pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name="YourAppName")
    img = qrcode.make(uri)

    # Save the image to a file
    qr_code_file = f"{username}_qr.png"
    img.save(qr_code_file)

    # Open the image file with the default image viewer
    os.system(f"open '{qr_code_file}'")  # For MacOS
    # Use this for Windows: os.system(f"start {qr_code_file}")
    # Use this for Linux: os.system(f"xdg-open {qr_code_file}")

def verify_totp_token(secret, token):
    """
    Verify a TOTP token against a secret.
    
    Args:
        secret (str): The TOTP secret.
        token (str): The token provided by the user.
    
    Returns:
        bool: True if the token is valid, otherwise False.
    """
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

def register_user(users):
    """
    Register a new user with a username, password, and 2FA via TOTP.
    
    Args:
        users (dict): The dictionary containing existing user data.
    """
    username = input("Enter a new username: ")
    if username in users:
        print("Username already exists.")
        return
    password = getpass.getpass("Enter a new password: ")
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Generate and display TOTP secret as QR code
    secret = generate_totp_secret()
    generate_qr_code(username, secret)
    print("Scan the QR code with your authenticator app.")

    # Generate a unique user ID
    user_id = str(uuid.uuid4())
    
    users[username] = {'id': user_id, 'hashed': hashed, 'secret': secret}
    save_user(username, hashed, secret, user_id)
    print(f"User registered successfully with ID {user_id} and 2FA.")

def login_user(users):
    """
    Log in an existing user with a username, password, and 2FA via TOTP.
    
    Args:
        users (dict): The dictionary containing existing user data.

    Returns:
        str: The username if login is successful, otherwise None.
    """
    username = input("Enter your username: ")
    password = getpass.getpass("Enter your password: ")
    user = users.get(username)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed']):
        # Uncomment the next section for 2FA validation
        
        token = input("Enter the 2FA token from your authenticator app: ")
        if verify_totp_token(user['secret'], token):
            print("Logged in successfully with 2FA!")
            return username
        else:
            print("Invalid 2FA token.")
            return None
    
        # Use this line for testing without 2FA
        print("Logged in successfully without 2FA!")
        return username
    else:
        print("Invalid username or password.")
        return None
