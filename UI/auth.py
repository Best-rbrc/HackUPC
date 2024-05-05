import bcrypt
import pyotp
import qrcode
import getpass
import os
import uuid

PASSWORD_FILE = "passwords.txt"

def load_users():
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
    with open(PASSWORD_FILE, "a") as file:
        file.write(f"{user_id}:{username}:{hashed.decode('utf-8')}:{secret}\n")

    user_file = f"{username}_data.txt"
    with open(user_file, "w") as file:
        file.write(f"ID: {user_id}\n")
        file.write(f"Username: {username}\n")
        file.write(f"Secret: {secret}\n")

def generate_totp_secret():
    return pyotp.random_base32()

def generate_qr_code(username, secret):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(username, issuer_name="YourAppName")
    img = qrcode.make(uri)
    qr_code_file = f"{username}_qr.png"
    img.save(qr_code_file)
    os.system(f"open '{qr_code_file}'")

def verify_totp_token(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

def register_user(users, username, password):
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    secret = generate_totp_secret()
    generate_qr_code(username, secret)
    user_id = str(uuid.uuid4())
    users[username] = {'id': user_id, 'hashed': hashed, 'secret': secret}
    save_user(username, hashed, secret, user_id)
    print(f"User registered successfully with ID {user_id} and 2FA.")

def login_user(users, username, password, token):
    user = users.get(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['hashed']):
        if verify_totp_token(user['secret'], token):
            print("Logged in successfully!")
            return username
        else:
            print("Invalid 2FA token.")
            return None
    else:
        print("Invalid username or password.")
        return None

if __name__ == "__main__":
    users = load_users()

    # Test Registration
    print("Testing Registration...")
    register_user(users, "test_user", "password123")

    # Test Login
    print("Testing Login...")
    token = input("Enter the 2FA token: ")
    login_user(users, "test_user", "password123", token)
